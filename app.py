import os
import base64
import streamlit as st
import shutil
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_option_menu import option_menu
from PIL import Image 
from docx import Document
from genai_report_generator.report_generator import report_gen
from genai_chatbot.chat_generator import chatbot
from genai_utils.genai_helper import get_conversation_chain


st.set_page_config(page_title="DataGenie",page_icon="🛢",layout="wide")

def remove_create_uploaded_file_chatbot_dir():
    """
    Check and remove directory audio_dir if exists and create empty directory
    """
    if os.path.exists(os.path.join(os.getcwd(),"genai_chatbot","uploaded_files")):
        shutil.rmtree(os.path.join(os.getcwd(),"genai_chatbot","uploaded_files"))
    os.makedirs(os.path.join(os.getcwd(),"genai_chatbot","uploaded_files"),exist_ok=True)


def session_init():
    if not hasattr(st.session_state,"chain_executed"):
        st.session_state.chain_executed = True

    if not hasattr(st.session_state,"pdf_chain_executed"):
        st.session_state.pdf_chain_executed = True

    if not hasattr(st.session_state,"genai_executed_check"):
        st.session_state.genai_executed_check = True

    if not hasattr(st.session_state,"generated_answer_check"):
        st.session_state.generated_answer_check = True

    if not hasattr(st.session_state,"doc"):
        st.session_state.doc = Document()

    if not hasattr(st.session_state,"doc_generate_check"):
        st.session_state.doc_generate_check = False

    if not hasattr(st.session_state,"vector_store_check"):
        st.session_state.vector_store_check = True
    
    if not hasattr(st.session_state,"chat_bot_interface_check"):
        st.session_state.chat_bot_interface_check = False

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "convo_chain" not in st.session_state:
        st.session_state.convo_chain = get_conversation_chain()


if __name__ == '__main__':
    session_init()

    st.markdown("""
            <style>
                .block-container {
                        padding-top: 2rem;
                        padding-bottom: 0rem;
                        padding-left: 2.5rem;
                        padding-right: 2.5rem;
                    } 
                
                .div.css-10qvep2.e1f1d6gn1 {
                height=10px !important;
                }
            </style>
            """, unsafe_allow_html=True)

    # for logo and header
    with st.container():
            col1,col2=st.columns([0.13,0.87],gap="large")
            with col1:
                logo_image = Image.open(".assests/DataGenie.png")
                resized_logo = logo_image.resize((280, 230))
                # Get the dimensions of the logo image
                logo_width, logo_height = resized_logo.size
                logo= st.image(resized_logo, use_column_width=False, output_format="auto", width=logo_width) 
            with col2:
                add_vertical_space(2)
                st.markdown("""# DataGenie  <span style='font-size:24px; color:orange'>- GenAI powered chatbot & report generator </span>""",unsafe_allow_html=True)
                st.divider()


    with st.container():
        col1,col2 = st.columns([0.18,0.82],gap="large")
        with col1:
            selected_nav= option_menu(
                    menu_title=None,
                    options=["Report Generator","Chatbot"],
                    icons = ["file-earmark-text","chat-square-dots"],
                    menu_icon="cast",
                    default_index=0,
                    orientation="vertical",
                    styles={"container": {"padding": "0.5!important","width":"100% !important"}}
                        )
        with col2:
            if selected_nav == "Report Generator":
                report_gen()

            if selected_nav == "Chatbot":
                chatbot()
