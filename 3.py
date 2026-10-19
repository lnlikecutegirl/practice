import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
# print("------->重新执行此文件，渲染展示页面")
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

system_prompt = """
    你叫%s，现在是用户的真实伴侣，请完全代入伴侣角色。：
    规则：
    1. 每次只回1条消息
    2. 禁止任何场景或状态描述性文字
    3. 匹配用户的语言
    4. 回复简短，像微信聊天一样
    5. 有需要的话可以用❤️🌸等emoji表情
    6. 用符合伴侣性格的方式对话
    7. 回复的内容, 要充分体现伴侣的性格特征
    伴侣性格：
    - %s
    你必须严格遵守上述规则来回复用户。
    """
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)



if "messages" not in st.session_state:
    st.session_state.messages = []

if "nick_name" not in st.session_state:
    st.session_state.nick_name = "小甜甜"
if "nature" not in st.session_state:
    st.session_state.nature = "活泼开朗的东北姑娘"

#左侧侧边栏
with st.sidebar:
    st.subheader('伴侣信息')
    nick_name=st.text_input('昵称',placeholder='请输入伴侣的昵称',value=st.session_state.nick_name)
    if nick_name:
        st.session_state.nick_name = nick_name
    nature=st.text_area('性格',placeholder='请输入伴侣性格',value=st.session_state.nature)
    if nature:
        st.session_state.nature = nature

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

    # print([{
    #     "role":"system","content":system_prompt},
    #     *st.session_state.messages
    #     ])
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role":"system","content":system_prompt % (st.session_state.nick_name,st.session_state.nature)},
            *st.session_state.messages
        ],
        stream=True
    )
    #非流氏输出的解析方式
    # print("<------大模型的返回结果:",resp.choices[0].message.content)
    # st.chat_message("assistant").write(resp.choices[0].message.content)

    #流式输出解析结果
    response_message=st.empty()
    full_response = ""
    for chunk in resp:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_response += content
            response_message.chat_message("assistant").write(full_response)

    st.session_state.messages.append({"role":"assistant","content":full_response})