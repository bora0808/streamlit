import streamlit as st
from openai import OpenAI
import os

openai_api_key = st.secrets["OPENAI_API_KEY"]
st.set_page_config(page_title="Jarinibot", page_icon="💬")

# CSS 스타일 적용
st.markdown(
    """
    <style>
    .chat-container {
        max-width: 700px;
        margin: 0 auto;
        
    }
    .chat-bubble {
        padding: 10px 15px;
        border-radius: 20px;
        margin: 10px 0;
        font-size: 16px;
        line-height: 1.5;
        width: fit-content;
        max-width: 80%;
    }
    .chat-bubble-user {
        background-color: #0084ff;
        color: white;
        align-self: flex-end;
        float: right;
    }
    .chat-bubble-assistant {
        background-color: #f0f0f0;
        color: black;
        align-self: flex-start;
    }
    .chat-input {
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("💬 Jarinibot")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "안녕하세요. 자리니입니다."}]

# 대화 메시지 출력
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    role_class = "chat-bubble-assistant" if msg["role"] == "assistant" else "chat-bubble-user"
    st.markdown(
        f'<div class="chat-bubble {role_class}">{msg["content"]}</div>',
        unsafe_allow_html=True,
    )
st.markdown('</div>', unsafe_allow_html=True)

# 사용자 입력 받기
if prompt := st.chat_input("궁금한 내용을 입력해 주세요."):

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(
        f'<div class="chat-bubble chat-bubble-user">{prompt}</div>',
        unsafe_allow_html=True,
    )

    # OpenAI API 호출
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state["messages"]
    )
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})

    # 챗봇의 응답 출력
    st.markdown(
        f'<div class="chat-bubble chat-bubble-assistant">{msg}</div>',
        unsafe_allow_html=True,
    )
