import streamlit as st
import requests

st.title("코드 생성 웹사이트")
st.write("여러 장의 이미지를 업로드하여 모델이 예측한 코드 조각을 하나의 코드 파일로 생성합니다.")

# 이미지 업로드
uploaded_files = st.file_uploader("이미지를 업로드하세요", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    st.write("업로드된 이미지:")
    code_snippets = []

    for uploaded_file in uploaded_files:
        st.image(uploaded_file, use_column_width=True)
        
        # FastAPI 서버에 이미지 업로드하여 예측 요청
        response = requests.post(
            "http://localhost:8000/predict/",
            files={"file": uploaded_file.getvalue()}
        )

        if response.status_code == 200:
            predicted_label = response.json().get("predicted_label")
            code_snippets.append(predicted_label)
        else:
            st.write(f"{uploaded_file.name} 예측 실패")

    # 하나의 코드 파일로 생성
    if code_snippets:
        full_code = "\n".join(code_snippets)
        st.write("생성된 코드:")
        st.code(full_code)

        # 코드 파일 다운로드
        st.download_button(
            label="코드 파일 다운로드",
            data=full_code,
            file_name="generated_code.py",
            mime="text/plain"
        )
