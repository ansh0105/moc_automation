# DataGenie

DataGenie is a powerful web application designed to automate two key processes:
1. **Report Generation**: Automatically generate PDF reports from CSV files with predefined structures, text summaries, tables, and charts.
2. **Interactive Chatbot**: Query and interact with personalized data, such as PDFs, using advanced AI features like memory retention and optimized search.


## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Report Generator](#report-generator)
  - [Chatbot](#chatbot)
- [Customization](#customization)



## Features
### Report Generator
- **Automated Report Creation**: Generate comprehensive reports based on predefined structures.
- **Text Summarization**: Automatically summarize key topics within your data.
- **Visualizations**: Integrate tables and charts seamlessly into your reports.
- **Editable Outputs**: Download and edit reports in Word format before finalizing.

### Chatbot
- **Data Interaction**: Upload reports and interact with them in real time.
- **Memory Retention**: Maintain the latest three states of interaction for continuity.
- **Advanced Search**: Leverage RAG query optimizers for enhanced search capabilities.
- **User-Friendly Interface**: Engage with data through a streamlined and intuitive UI.

## Prerequisites

- Python 3.9 (or above)
- Virtual Environment (optional but recommended)
- Azure OpenAI credentials


## Installation
To get started with DataGenie, follow the steps below:

1. **Clone the Repository**:
    ```bash
    git clone <repository-url>
    ```

2. **Create and Activate Python Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration
### Azure OpenAI Setup
You need to update the `.env` file under the `genai_utilits` directory with your Azure OpenAI credentials. You can obtain these credentials from [here](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/create-resource?pivots=web-portal).

 Example configuration for `.env`:
  ```env
  OPENAI_API_KEY=<your_azure_openai_api_key>
  OPENAI_API_TYPE=<your_azure_openai_type e.g azure>
  OPENAI_API_VERSION=<your_azure_openai_version>
  OPENAI_ENDPOINT=<your_azure_openai_endpoint>
  
  ```

## Usage
**After completing the configuration, start the Streamlit application:**
```bash
streamlit run app.py
```
The Streamlit app will be accessible in your web browser, where you can upload files for report generation and chatbot.


### Report Generator

1. **Upload CSV File**:
    - Upload your export-import data CSV file. A sample file (`dec_com_export.csv`) is available in the `.assets` folder.

2. **Generate Report**:
    - The tool will generate a PDF and Word file stored in the `generated_report` folder.

3. **Predefined Structure of the Report**:
    - **Overall export trends**
    - **Top five export commodities**
    - **Export growth rates**
    - **Sector-wise analysis**
    - **Commodities comparison**

**Here is a demonstration video of DataGenie Report Generator in action:**

[](https://github.com/user-attachments/assets/0d08458a-bbbe-4d6d-b88e-4b93cda9e88c)

### Chatbot

1. **Upload Report**:
    - Upload a PDF report (e.g., `Introduction To New Gen Technology.pdf` located in the `.assets` folder).

2. **Chat with the Data**:
    - The process involves fetching data from the PDF, initializing VectorStore, preparing data for embeddings, and starting the chat. The latest three memory states are retained for continuity.
  
**Here is a demonstration video of DataGenie ChatBot in action:**

[](https://github.com/user-attachments/assets/805f0731-cdaa-4213-b024-e3eda524082b)

## Customization

 1. **Modify Chat Avatars:**
    - To change the avatars in the chatbot, add new images to the `.assets` directory.
  
 2. **UI Customization:**
    - UI customization options are available in the `config.toml` file located in the       `.streamlit` directory.
    Modify the appearance and settings of the Streamlit app as needed.


