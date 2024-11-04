import streamlit as st
import json

# JSON 파일 불러오기
with open('problems.json', 'r', encoding='utf-8') as file:
    problems = json.load(file)

# 세션 상태 초기화
if "user_prompt" not in st.session_state:
    st.session_state.user_prompt = {}
if "formatted_prompt" not in st.session_state:
    st.session_state.formatted_prompt = {}

# 모든 문제 키를 초기화
for key in problems.keys():
    if key not in st.session_state.user_prompt:
        st.session_state.user_prompt[key] = []
    if key not in st.session_state.formatted_prompt:
        st.session_state.formatted_prompt[key] = ""

# 페이지 설정
st.set_page_config(page_title="프로그래밍 문제 풀이 검증", layout="centered")

# 탭 형식으로 페이지 선택 옵션 구현
tabs = st.tabs(list(problems.keys()))

# 각 탭에 대해 문제 설명, 코드 입력, 답안 제출 등을 구현
for tab, (problem_key, problem_data) in zip(tabs, problems.items()):
    with tab:
        st.header(problem_data["description"]["header"])
        st.markdown(problem_data["description"]["problem"])

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(problem_data["description"]["input_desc"])
        with col2:
            st.markdown(problem_data["description"]["output_desc"])

        st.markdown("---")

        col3, col4 = st.columns(2)
        with col3:
            st.markdown(problem_data["description"]["input_example"])
        with col4:
            st.markdown(problem_data["description"]["output_example"])

        # 코드 입력을 위한 버튼
        st.subheader("코드 입력")
        columns = st.columns(3)
        for i, code in enumerate(problem_data["class_list"]):
            col = columns[i % 3]
            with col:
                if st.button(code, key=f"{problem_key}_{code}"):
                    st.session_state.user_prompt[problem_key].append(code)
                    st.session_state.formatted_prompt[problem_key] = problem_data["prompt_template"].format(
                        "\n".join(st.session_state.user_prompt[problem_key][:-1]),
                        st.session_state.user_prompt[problem_key][-1] if st.session_state.user_prompt[problem_key] else ""
                    )

        # 코드 형식 출력 (들여쓰기 적용)
        formatted_code_display = st.session_state.formatted_prompt[problem_key].replace("\n", "\n    ")
        st.text_area("입력된 코드", value=formatted_code_display, height=100, key=f"{problem_key}_text_area")

        # 답안 제출과 초기화 버튼
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("답안 제출", key=f"{problem_key}_submit"):
                if st.session_state.formatted_prompt[problem_key].replace(" ", "").strip() == problem_data["answer"].replace(" ", "").strip():
                    st.markdown(
                        '<div style="background-color:green; padding:5px; border-radius:3px; color:white; text-align:center; display:inline-block; font-size:14px;">정확한 풀이</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        '<div style="background-color:red; padding:5px; border-radius:3px; color:white; text-align:center; display:inline-block; font-size:14px;">잘못된 풀이</div>',
                        unsafe_allow_html=True
                    )

        with col2:
            if st.button("답안 초기화", key=f"{problem_key}_reset"):
                st.session_state.user_prompt[problem_key] = []
                st.session_state.formatted_prompt[problem_key] = ""
