
import logging
import streamlit as st

_MODELS=[
        'mixtral-8x7b-32768',
        'llama2-70b-4096',
    ]
def st_options():
    
    with st.expander("可选配置"):
        model = st.selectbox("选择模型",
                             index=0,
                             options=_MODELS)
        content = st.text_area("人格设定",
                               value=st.session_state.config['messages'][0]["content"])
        stream = st.toggle("Stream",
                           value=st.session_state.config["stream"])
        temperature=st.slider("temperature",
                              min_value=0.0,
                              value=st.session_state.config["temperature"],
                              step=0.1,
                              max_value=1.0)
        top_p=st.slider("top_p",
                              min_value=0.0,
                              value=st.session_state.config["top_p"],
                              step=0.1,
                              max_value=1.0)
        max_tokens=st.slider("max_tokens",
                              min_value=100,
                              value=st.session_state.config["max_tokens"],
                              step=100,
                              max_value=32768)
        return {
            "messages":[
                {
                    "role": "assistant",
                    "content": content
                }
            ],
            "model":model,
            "stream":stream,
            "temperature":temperature,
            "top_p":top_p,
            "max_tokens":max_tokens
        }
def create_sidebar(config:dict[str,object]):
    logging.info("创建侧边栏...")
    with st.sidebar:
        st.subheader("环境配置")
        if "config" not in st.session_state:
            st.session_state.config = config
        with st.form("form1"):
            api_key = st.text_input("API_KEY",
                                    type="password",
                                    value=st.session_state.config["api_key"])
            options = st_options()
            if st.form_submit_button("保存配置"):
                st.session_state.config.update({"api_key":api_key})
                st.session_state.config.update(options)
                logging.debug(f"表单保存的配置信息：{st.session_state.config}")

        
       
