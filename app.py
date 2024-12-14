import streamlit as st
from openai import OpenAI

# 페이지 제목 설정
st.title("카페 노비 챗봇(프로토타입)")

# 사용자로부터 API 키 입력 받기
api_key = st.text_input("API 키를 입력하세요:", type="password")

# 입력된 API 키를 세션 상태에 저장
if api_key:
    st.session_state["api_key"] = api_key

# API 클라이언트 초기화
if "api_key" in st.session_state:
    client = OpenAI(api_key=st.session_state["api_key"])

# 챗봇 설정 메시지
system_message = '''
챗봇 설정
이름:김노비
업무:카페 문의대응
나이:23세
특징1:조선시대 노비처럼 대화함
특징2:자신을 표현할땐 "소인"이란 말을 사용하며 다른 사람을 표현할땐 "선비님"란 말을씀
특징3:가격 질문시 세트메뉴가 저렴하다는 홍보를 많이함

카페 설정
카페 이름:조카(조선 카페의 약자)
배경:조선 후반
업무 방식:문의 김노비 이외의 직원들이 3교대로 일함, 선불제
단일 메뉴:유자차(가격:6포), 율무차(가격:5포), 핫초코(가격:5포), 호빵(가격:4포), 유과(가격:4포), 약과(가격:4포)
세트 메뉴:임금님의 수라상(음료1+디저트1 가격:8포), 새참(디저트2 가격:7포)
'''

# 시스템 메시지 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_message}]

# 챗 메시지 출력
for idx, message in enumerate(st.session_state.messages):
    if idx > 0:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 사용자 입력 받기
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # OpenAI 모델 호출
    if "api_key" in st.session_state:
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})