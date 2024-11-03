from fastapi import FastAPI, UploadFile, File
import torch
import torch.nn as nn
from PIL import Image, UnidentifiedImageError
import io
from torchvision import transforms
from crnn import CRNN  # crnn.py에서 CRNN 클래스 불러오기
from sklearn.preprocessing import LabelEncoder

# FastAPI 인스턴스 생성
app = FastAPI()

# 모델 및 디바이스 설정
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_path = './model/code_classifier_20241102.pth'
num_classes = 9  # 실제 클래스 수 (리스트 크기)로 수정 필요
model = CRNN(num_classes=num_classes)
model.load_state_dict(torch.load(model_path, map_location=device))
model.to(device)
model.eval()

# 클래스 리스트 (학습한 데이터셋의 클래스)
class_list = ["a,b=input().split('-')", 'a=int(a)', 'b=int(b)', 'n-=1', 'n=int(input())',
              'print(a+b)', 'print(bool(a) == bool(b))', 'print(n)', 'while n!=0']

# LabelEncoder 설정
label_encoder = LabelEncoder()
label_encoder.fit(class_list)

# 이미지 전처리 설정
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

# 이미지 예측 함수
def predict_image(model, image, transform, device, label_encoder):
    image_tensor = transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        output = model(image_tensor)
        _, predicted = torch.max(output, 1)
        predicted_label = label_encoder.inverse_transform([predicted.item()])[0]
    return predicted_label

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    try:
        image = Image.open(io.BytesIO(await file.read())).convert('RGB')
        predicted_label = predict_image(model, image, transform, device, label_encoder)
        return {"predicted_label": predicted_label}
    except UnidentifiedImageError:
        return {"error": "Invalid image format"}
