
from langchain_community.document_loaders import ObsidianLoader
import logging
import streamlit as st

@st.cache_data(show_spinner="正在从Obsidian中加载文档...")
def load_documents_from_obsidian(obsidian_file_path:str):
    logging.info("开始从GitHub加载文档....")
    documents = ObsidianLoader(obsidian_file_path).load()
    logging.debug(f"测试Obsidian加载到的文档：{documents[0]}")
    return documents


