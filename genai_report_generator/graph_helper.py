import os
import pandas as pd
import matplotlib.pyplot as plt
moc_automation_dir_path = "/".join(os.path.abspath(__file__).split('\\')[:-2])


def overall_export_comp(df: pd.DataFrame,fig_name: str):
    """
    To create bar chart of overall export
    """
    total_dec_22 = df[df.columns[2]].sum()
    total_dec_23 = df[df.columns[4]].sum()
    print(total_dec_22,total_dec_23)

    # Plotting the data
    plt.figure(figsize=(10, 6))
    plt.bar([df.columns[2], df.columns[4]], [total_dec_22, total_dec_23], color=['blue', 'orange'],alpha= 0.7)
    plt.title(f"Total Export Value Comparison for {df.columns[2][:-24]} and {df.columns[4][:-24]}")
    plt.xlabel("Year")
    plt.ylabel("Total Export Value (Million USD)")
    plt.savefig(os.path.join(moc_automation_dir_path,"custom_generated_charts", fig_name+".png"))


def top_export_commodities(df: pd.DataFrame,fig_name: str):
    """
    To create bar chart of top export commodities
    """
    # Sort the DataFrame by the export values for December 2023
    top_commodities = df.sort_values(by= df.columns[4], ascending=False)

    top_commodities = top_commodities.head(5)
    print(top_commodities[[df.columns[1],df.columns[2],df.columns[4]]])

    plt.figure(figsize=(12, 6))
    bar_width = 0.35
    index = range(len(top_commodities))
    plt.bar(index, top_commodities[df.columns[2]], bar_width, color='blue',alpha= 0.6, label=df.columns[2][:-24])
    plt.bar([i + bar_width for i in index], top_commodities[df.columns[4]], bar_width, color='orange', alpha= 0.8, label=df.columns[4][:-24])

    for i in index:
        plt.text(i, top_commodities[df.columns[2]].iloc[i] + 10, str(top_commodities[df.columns[2]].iloc[i]), ha='center', va='bottom')
        plt.text(i + bar_width, top_commodities[df.columns[4]].iloc[i] + 10, str(top_commodities[df.columns[4]].iloc[i]), ha='center', va='bottom')

    plt.xlabel("Commodities")
    plt.ylabel("Export Value (Million USD)")
    plt.title(f"Top Export Commodities Comparison between {df.columns[2][:-24]} and {df.columns[4][:-24]}")
    plt.xticks([i + bar_width / 2 for i in index], top_commodities["Commodities"])
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(moc_automation_dir_path,"custom_generated_charts", fig_name+".png"))


def max_com_export_gr(df_gr: pd.DataFrame, fig_name: str):
    """
    To create bar chart of maximum export
    """
    top_5_commodities = df_gr

    # Create a bar chart
    plt.figure(figsize=(12, 6))
    bars = plt.bar(top_5_commodities['Commodities'], top_5_commodities['Growth Rate'], color='blue', alpha= 0.6)
    plt.xlabel('Commodities')
    plt.ylabel('Growth Rate (%)')
    plt.title('Top 5 Commodities with Highest Growth Rates (Dec 2022 to Dec 2023)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.5, round(yval, 2), ha='center', va='bottom')
    plt.savefig(os.path.join(moc_automation_dir_path,"custom_generated_charts", fig_name+".png"))


def min_com_export_gr(df_gr: pd.DataFrame, fig_name: str):
    """
    To create bar chart of minimum export group
    """
    top_5_min_growth = df_gr
    plt.figure(figsize=(12, 6))
    bars= plt.barh(top_5_min_growth['Commodities'], top_5_min_growth['Growth Rate'], color='blue', alpha= 0.6)
    plt.xlabel('Commodities')
    plt.ylabel('Growth Rate (%)')
    plt.title('Top 5 Commodities with Minimum Growth Rates (Dec 2022 to Dec 2023)')

    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height() / 2, '{:.2f}%'.format(width),
                va='center', ha='left', color='black')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(moc_automation_dir_path, "custom_generated_charts", fig_name+".png"))


def sector_wise_distribution(df: pd.DataFrame, fig_name: str):
    """
    To create pie chart of sector wise distribution
    """
    top_10_commodities = df.sort_values(by=[df.columns[5]], ascending=True)
    top_10_commodities = df.head(10)

    print(top_10_commodities[[df.columns[1],df.columns[5],df.columns[3]]].head(5))
    
    plt.figure(figsize=(12, 8))
    plt.pie(top_10_commodities[top_10_commodities.columns[5]], labels=top_10_commodities[top_10_commodities.columns[1]], autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    plt.title(f'Distribution of Export Values Among Different Sectors for {top_10_commodities.columns[5][:-24]}')
    plt.savefig(os.path.join(moc_automation_dir_path,"custom_generated_charts", fig_name+".png"))


def commodities_comparision(df: pd.DataFrame, fig_name: str):
    """
    To create bar chart of commodities comparision
    """
    top_commodities = df.sort_values(by= df.columns[5], ascending=False)
    top_commodities = df.head(5)
    

    plt.figure(figsize=(12, 6))
    bar_width = 0.35
    index = range(len(top_commodities))
    plt.bar(index, top_commodities[df.columns[3]], bar_width, color='blue',alpha= 0.6, label=df.columns[3][:-24])
    plt.bar([i + bar_width for i in index], top_commodities[df.columns[5]], bar_width, color='orange', alpha= 0.8, label=df.columns[5][:-24])

    # Adding the values on top of the bars
    for i in index:
        plt.text(i, top_commodities[df.columns[3]].iloc[i] + 10, str(top_commodities[df.columns[3]].iloc[i]), ha='center', va='bottom')
        plt.text(i + bar_width, top_commodities[df.columns[5]].iloc[i] + 10, str(top_commodities[df.columns[5]].iloc[i]), ha='center', va='bottom')

    plt.xlabel("Commodities")
    plt.ylabel("Export Value (Million USD)")
    plt.title(f"Top Export Commodities Comparison between {df.columns[3][:-24]} and {df.columns[5][:-24]}")
    plt.xticks([i + bar_width / 2 for i in index], top_commodities["Commodities"])
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(moc_automation_dir_path,"custom_generated_charts", fig_name+".png"))