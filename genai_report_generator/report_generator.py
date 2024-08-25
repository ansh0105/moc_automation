import os
import sys
import time
import base64
import pandas as pd
import streamlit as st
moc_automation_dir_path = "/".join(os.path.abspath(__file__).split('\\')[:-2])
sys.path.insert(0, moc_automation_dir_path)

from genai_utils.genai_helper import get_non_rtr_convo_chain
from genai_utils.prompts import PDF_STRUCTURE_PROMPT_V3 
from genai_report_generator.struct_manager import get_response



def report_gen():
    """
    Funtion helps to generate report in a predefine structure
    1. Upload csv file
    2. Initialize textual chain 
    3. Generate content for report
    4. Render report
    """
    # Upload CSV files
    st.session_state.uploaded_files = st.file_uploader("Choose CSV files to upload", type=['csv'], accept_multiple_files=True)
    os.makedirs(os.path.join(moc_automation_dir_path, "uploads"),exist_ok=True)
    os.makedirs(os.path.join(moc_automation_dir_path, "custom_generated_charts"),exist_ok=True)
    os.makedirs(os.path.join(moc_automation_dir_path, "custom_generated_tables"),exist_ok=True)
    os.makedirs(os.path.join(moc_automation_dir_path, "generated_report"),exist_ok=True)

    st.session_state.button = st.button("Submit",key="b1")
    if st.session_state.uploaded_files and st.session_state.button:
        
        with st.status("Initializing Report Generation Process..........", expanded=True) as status:
            st.write("Uploading Files...")
            st.session_state.combined_file_data = ""

            for file in st.session_state.uploaded_files:
                file_name = file.name       
                file_path = os.path.join(moc_automation_dir_path,"uploads", file_name)
                with open(file_path, "wb") as f:
                    f.write(file.getbuffer())

                st.session_state.combined_file_data += file.getvalue().decode("utf-8")+ "\n \n"
                st.session_state.uploaded_dataframe = pd.read_csv(file_path)

            with open(os.path.join(moc_automation_dir_path,"uploads", "merged_data_file.txt"),'w') as f:
                f.write(st.session_state.combined_file_data)


            st.write("Intializing Agent Chains...")
            if st.session_state.pdf_chain_executed:
                # custom pdf structure: rule based
                st.session_state.pdf_structure_chain = PDF_STRUCTURE_PROMPT_V3

                with open(os.path.join(moc_automation_dir_path,"uploads", "merged_data_file.txt"), 'r', encoding='utf-8') as f:
                    st.session_state.merged_data = f.read()
                # to extract texual information
                st.session_state.text_data_chain =  get_non_rtr_convo_chain()
                st.session_state.pdf_chain_executed = False 

                     
            st.write("Generating answer from initialised chain...")
            if st.session_state.button or st.session_state.generated_answer_check:
                st.session_state.doc_generate_check = get_response(st.session_state.merged_data, st.session_state.uploaded_dataframe)
                st.session_state.generated_answer_check = False    
               
            status.update(
                label="Process Complete!", state="complete", expanded=False
            )        

        if st.session_state.doc_generate_check:
            with open(os.path.join(moc_automation_dir_path,"generated_report","gen_report.pdf"), "rb") as f:
                pdf_data = f.read()
            b64_pdf = base64.b64encode(pdf_data).decode("utf-8")                    
            pdf_display = f'''<div style="background-color: #0E1117; padding: 10px;"> 
                            <iframe src="data:application/pdf;base64,{b64_pdf}" width="85% !important" height="550 !important" frameborder="0">
                            </iframe>
                            </div>'''
            st.markdown(pdf_display, unsafe_allow_html=True)

            


    


