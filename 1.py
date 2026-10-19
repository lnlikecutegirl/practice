import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get('DEEPSEEK_API_KEY')

st.set_page_config(
    page_title="AI智能伴侣",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}
)

st.title('AI智能伴侣')

st.logo('./resources/logo.png')

system_prompt = "你是一个非常可爱的AI助理，你的名字叫小甜甜，请你使用温柔可爱的语气回答用户的问题"

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])
    # if message["role"] == "user":
    #     st.chat_message("user").write(message["content"])
    # else:
    #     st.chat_message("assistant").write(message["content"])

prompt=st.chat_input('请输入你的问题：')
if prompt:
    st.chat_message("user").write(prompt)
    print("--------->调用ai大模型，提示词：",prompt)
    #st.chat_message("assistant").write("正在思考中...")
    st.session_state.messages.append({"role":"user","content":prompt})

    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role":"system","content":system_prompt},
            {"role":"user","content":prompt}
        ]
    )
    print("<------大模型的返回结果:",resp.choices[0].message.content)
    st.chat_message("assistant").write(resp.choices[0].message.content)
    st.session_state.messages.append({"role":"assistant","content":resp.choices[0].message.content})
