import os
import time
import sys
import regex as re
import pandas as pd
import streamlit as st
from datetime import datetime
from docx2pdf import convert

moc_automation_dir_path = "/".join(os.path.abspath(__file__).split('\\')[:-2])
sys.path.insert(0, moc_automation_dir_path)

from genai_report_generator.doc_helper import format_paragraph, format_image, WD_ALIGN_PARAGRAPH
from genai_utils.prompts import OVERALL_EXPORT_PROMPT,COM_COMPARISION_PROMPT, TOP_EXPORT_COM_PROMPT,SECTOR_ANALYSIS_PROMPT
from genai_report_generator.graph_helper import top_export_commodities, overall_export_comp, sector_wise_distribution,commodities_comparision
from genai_report_generator.table_helper import export_growth_rate_table


def gen_struct_heading(uploaded_file_data :str, content :str, dataframe: pd.DataFrame):
    """
    Function to generate content for overall export heading and structure those content in doc file
    """
    response =  st.session_state.text_data_chain.predict(input = OVERALL_EXPORT_PROMPT.format(
                                                        uploaded_file_data,
                                                        dataframe.columns[2],
                                                        dataframe[dataframe.columns[2]].sum(),
                                                        dataframe.columns[4],
                                                        dataframe[dataframe.columns[4]].sum() ))
    format_paragraph(content.strip(),"Times New Roman", 14, 2, True, WD_ALIGN_PARAGRAPH.LEFT)
    format_paragraph(response, "Times New Roman", 12 ,1)


def gen_struct_top_five_export_commodities(content:str, dataframe: pd.DataFrame):
    """
    Function to generate and structure content for top five export commodities in doc file
    """
    top_commodities = dataframe.sort_values(by= dataframe.columns[4], ascending=False)
    top_commodities = top_commodities.head(5)
    response =  st.session_state.text_data_chain.predict(input = TOP_EXPORT_COM_PROMPT.format(
                                            top_commodities,
                                            dataframe.columns[2][:-24],
                                            dataframe.columns[4][:-24] ))
    
    format_paragraph( content, "Times New Roman", 14 ,2, True)
    format_paragraph(response, "Times New Roman", 12, 1)


def gen_struct_sector_wise_analysis(content:str, dataframe: pd.DataFrame):
    """
    Function to generate and structure content for sector wise analysis in doc file
    """
    top_10_commodities = dataframe.sort_values(by=[dataframe.columns[5]], ascending=True)
    top_10_commodities = dataframe.head(10)

    response =  st.session_state.text_data_chain.predict(input = SECTOR_ANALYSIS_PROMPT.format(
                                            top_10_commodities,
                                            dataframe.columns[5][:-24],
                                            ))
    format_paragraph(content, "Times New Roman", 14, 2,True)
    format_paragraph(response, "Times New Roman", 12, 1)


def gen_struct_commodities_comparision(content:str, dataframe: pd.DataFrame):
    """
    Function to generate and structure content for commodities comaparision in doc file
    """
    top_commodities = dataframe.sort_values(by= dataframe.columns[5], ascending=False)
    top_commodities = dataframe.head(5)

    response =  st.session_state.text_data_chain.predict(input = COM_COMPARISION_PROMPT.format(
                                            top_commodities,
                                            dataframe.columns[3][:-24],
                                            dataframe.columns[5][:-24]
                                            ))
    format_paragraph( content, "Times New Roman", 14, 2, True)
    format_paragraph(response, "Times New Roman", 12, 1)


def structure_graph(graph_path :str):
    """
    Function to structure graph/chart in doc file
    """
    format_image(graph_path, 16)


def get_response(uploaded_file_data:str, dataframe: pd.DataFrame) -> bool:
    """
    Function to generate and structure content inclding heading, graphs, table, graph content table content for the report.

    """
    
    format_paragraph("Government of India\nMinistry of Commerce & Industry\nDepartment of Commerce\nEconomic Division",
                     "Times New Roman", 16, 0, True, WD_ALIGN_PARAGRAPH.CENTER)
    format_paragraph(f"New Delhi, Dated {datetime.now().strftime('%dth %B, %Y')}","Times New Roman",8,0, True,WD_ALIGN_PARAGRAPH.RIGHT)

    elements = re.findall(r'(#heading|#table|#graph|#sub-heading): (.*?)(?=\n#|$)', st.session_state.pdf_structure_chain, re.DOTALL)

    for element in elements:
        element_type = element[0]
        element_content = element[1]

        if element_type in "#heading":
            gen_struct_heading(uploaded_file_data, element_content, st.session_state.uploaded_dataframe)

        elif element_type in "#table":
            if element_content.strip() in "Export growth rates":
                format_paragraph(element_content.strip(), "Times New Roman", 14, 2, True)
                export_growth_rate_table(dataframe, "export_growth_rates")

        elif element_type in "#graph":
            if element_content.strip() in "Overall export trends":
                overall_export_comp(st.session_state.uploaded_dataframe, "overall_export_trends")
                structure_graph(os.path.join(moc_automation_dir_path,"custom_generated_charts", "overall_export_trends"+".png"))

            elif element_content.strip() in "Top five export commodities":
                gen_struct_top_five_export_commodities(element_content.strip(), dataframe)
                top_export_commodities(st.session_state.uploaded_dataframe, "top_five_export_com")
                structure_graph(os.path.join(moc_automation_dir_path,"custom_generated_charts", "top_five_export_com"+".png"))

            elif element_content.strip() in "Sector-wise analysis":
                gen_struct_sector_wise_analysis(element_content.strip(), dataframe)
                sector_wise_distribution(st.session_state.uploaded_dataframe, "sector_wise_distribution")
                structure_graph(os.path.join(moc_automation_dir_path,"custom_generated_charts", "sector_wise_distribution"+".png"))
            

            elif element_content.strip() in "Commodities comparison":
                gen_struct_commodities_comparision(element_content.strip(), dataframe)
                commodities_comparision(st.session_state.uploaded_dataframe, "commodities_comparision")
                structure_graph(os.path.join(moc_automation_dir_path,"custom_generated_charts", "commodities_comparision"+".png"))
 
    st.session_state.doc.save(os.path.join(moc_automation_dir_path,"generated_report","gen_report.docx"))
    time.sleep(1)
    convert(os.path.join(moc_automation_dir_path,"generated_report","gen_report.docx"),
            os.path.join(moc_automation_dir_path,"generated_report","gen_report.pdf"))
    st.session_state.doc_generate_check = True
    return st.session_state.doc_generate_check