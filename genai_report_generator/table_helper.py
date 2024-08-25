import os
import sys
moc_automation_dir_path = "/".join(os.path.abspath(__file__).split('\\')[:-2])
sys.path.insert(0, moc_automation_dir_path)
import streamlit as st
from genai_report_generator.doc_helper import format_image,format_table,format_paragraph
from genai_report_generator.graph_helper import max_com_export_gr, min_com_export_gr
from genai_utils.prompts import EXPORT_GROWTH_RATE_PROMPT


def export_growth_rate_table(df, table_name):
    """
    Function to generate and structure content of table for export growth rates
    """
    df['Growth Rate'] = ((df[df.columns[4]] - df[df.columns[2]]) / df[df.columns[2]]) * 100
    result_table = df[['Commodities', 'Growth Rate']]
    result_table.to_csv(os.path.join("custom_generated_tables", table_name +".csv"), index =False)
    
    df_sorted = result_table.sort_values(by='Growth Rate', ascending=False)
    # Select the top 5 commodities
    top_5_max_growth = df_sorted.head(5)
    top_5_min_growth = result_table.nsmallest(5, 'Growth Rate')

    response =  st.session_state.text_data_chain.predict(input = EXPORT_GROWTH_RATE_PROMPT.format(
                                                        top_5_min_growth,
                                                        df.columns[2][:-24],
                                                        df.columns[4][:-24],
                                                        top_5_max_growth,
                                                        df.columns[2][:-24],
                                                        df.columns[4][:-24]))
    format_paragraph(response, "Times New Roman", 12,1)
    format_table(os.path.join(moc_automation_dir_path,"custom_generated_tables", table_name +".csv"))
    max_com_export_gr(top_5_max_growth, "top_five_maximum_commodity_gr")
    min_com_export_gr(top_5_min_growth, "top_five_minimum_commodity_gr")
    format_image(os.path.join(moc_automation_dir_path,"custom_generated_charts", "top_five_maximum_commodity_gr"+".png"), 14)
    format_image(os.path.join(moc_automation_dir_path,"custom_generated_charts", "top_five_minimum_commodity_gr"+".png"), 14)



