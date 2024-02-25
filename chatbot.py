
import logging
from groq import Groq
import yaml
import streamlit as st
from sidebar import create_sidebar
PROD_CONFIG_FILE = "config.yml"
DEV_CONFIG_FILE = "config-dev.yml"

@st.cache_data(show_spinner=False)
def load_config(file_path:str):
   
    logging.info("开始加载配置文件...")
    
    with open(file=file_path,mode="r",encoding="utf-8")as file:
        config = yaml.load(file,yaml.SafeLoader)
    logging.debug(f"读取配置文件内容：{config}")
    return config

def create_chat_completion():
    if st.session_state.config:
        config = st.session_state.config
    client = Groq(api_key=config["api_key"])
    if client is None:
        raise Exception("groq客户端初始化失败。")
    logging.debug(f"groq客户端初始化成功:{client}")
    messages = config["messages"]+(st.session_state.messages)
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=config["model"],
        temperature=config["temperature"],
        max_tokens=config["max_tokens"],
        top_p=config["top_p"],
        stop=config["stop"],
        stream=config["stream"])
    logging.debug(f"初始化聊天引擎完成:{chat_completion}")
    return chat_completion
        
def create_chat_bot():
    logging.info("创建聊天机器人...")
    st.title(":robot_face: Obsidian-Chat-Bot")
    #初始化聊天记录
    if "messages" not in st.session_state:
        st.session_state.messages = []

    #显示聊天记录
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

    #问题输入框
    if prompt := st.chat_input(placeholder="请输入"):
        #构造聊天记录对象
        st.session_state.messages.append({"role":"user","content":prompt})

        #显示用户输入的问题
        with st.chat_message("user"):
            st.markdown(prompt)

        #显示机器人响应的答案
        response = ""
        with st.chat_message("assistant"):
            placeholder = st.empty()
            for chunk in create_chat_completion():
                response += (chunk.choices[0].delta.content or "")
                placeholder.markdown(response + "|")
            placeholder.markdown(response)
        st.session_state.messages.append({"role":"assistant","content":response})

def run(deploy:bool,log_level:int):
    logging.basicConfig(level=log_level,
                    format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("程序启动...")
    #获取默认配置
    file_path = PROD_CONFIG_FILE if deploy else DEV_CONFIG_FILE
    config = load_config(file_path)
    #创建侧边栏，获取用户自定义配置
    create_sidebar(config['groq'])
    logging.info(f"当前会话中的配置信息：{st.session_state.config}")
    #创建聊天机器人
    create_chat_bot()







