import os
import sys
import time
moc_automation_dir_path = "/".join(os.path.abspath(__file__).split('\\')[:-2])
sys.path.insert(0, moc_automation_dir_path)
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from PIL import Image 
from docx import Document
from genai_utils.ChromaDBManager import ChromaDBManager
from genai_utils.genai_helper import data_preprocessing, rephrase_conversation
from genai_utils.prompts import CHATBOT_PROMPT



def response_generator(response: str):
    """
    Helps to Streamed response emulator
    """
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


def chatbot():
    uploaded_file = st.file_uploader("Choose files to upload", type=['pdf'], accept_multiple_files=False)
    submit_btn = st.button('Upload', key ='u1')

    if submit_btn and uploaded_file :
        uploaded_folder_path = os.path.join(os.getcwd(),"genai_chatbot","uploaded_files")
        merged_folder_path = os.path.join(os.getcwd(), "genai_chatbot", "uploaded_files")
        os.makedirs(uploaded_folder_path, exist_ok=True)

        uploaded_file_path = os.path.join(uploaded_folder_path, uploaded_file.name)
        # merged_file_path = os.path.join(merged_folder_path, "merged_uploaded_data.txt")

        # Save the file to the local directory
        with open(uploaded_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
    

        with st.status("Initializing Vector Store Process..........", expanded=True) as status:

            st.write("Fetching data from pdf...")
            file_data = data_preprocessing(uploaded_file_path, merged_folder_path)

            st.write("Initializing VectorStore... ")
            time.sleep(0.5)
            manager = ChromaDBManager()

            st.write("Prepare data for embeddings... ")
            time.sleep(0.5)
            doc,meta,embed,ids = manager.create_data(file_data)

            st.write("Initializing embedding... ")
            manager.push_data(doc,meta,embed,ids)


            status.update(
                label="Process Complete!", state="complete", expanded=False
            )
        st.session_state.chat_bot_interface_check = True


    if st.session_state.chat_bot_interface_check:
        manager = ChromaDBManager()
        with st.container(height=500):
            for message in st.session_state.messages:
                with st.chat_message(name=message["role"],avatar=message["avatar"]):
                    st.markdown(message["content"])

            # Accept user input
            if prompt := st.chat_input("Ask......"):
                rephrased_query = rephrase_conversation(chat_history=st.session_state.convo_chain.memory.load_memory_variables({}),query = prompt)

                st.session_state.messages.append({"role": "user","avatar":".assests/user.png", "content": prompt})

                with st.chat_message("user", avatar=".assests/user.png"):
                    st.markdown(prompt)

                with st.spinner("Thinking..."):
                    result = manager.query_data(rephrased_query)

                    llm_response = st.session_state.convo_chain.predict(input = CHATBOT_PROMPT.format(rephrased_query, result["documents"],result["metadatas"]))

                with st.chat_message("assistant",avatar=".assests/assistant.png"):
                    response = st.write_stream(response_generator(llm_response))

                st.session_state.messages.append({"role": "assistant", "avatar":".assests/assistant.png","content": response})

                if len(st.session_state.messages) >= 6:
                    st.session_state.messages = st.session_state.messages[2:]






