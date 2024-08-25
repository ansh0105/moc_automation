import os
from dotenv import load_dotenv
from langchain_community.chat_models import AzureChatOpenAI
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory
from langchain.chains.conversation.base import ConversationChain
import PyPDF2
import shutil
from genai_utils.prompts import REPHRASE_QUES_PROMPT



load_dotenv(override= True)
os.environ["OPENAI_API_TYPE"] = os.getenv("OPENAI_API_TYPE")
os.environ["OPENAI_API_VERSION"] = os.getenv("OPENAI_API_VERSION")
os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_API_BASE")
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')


def get_non_rtr_convo_chain() -> ConversationChain:
    """
    For initilazing non rerieval chain for llm
    """
    llm = AzureChatOpenAI(deployment_name="gpt-4-turbo",model_name="gpt-4-turbo",temperature=0,presence_penalty=0,frequency_penalty = 0)
    memory = ConversationBufferMemory()
    conversation_chain = ConversationChain(
        llm=llm,
        memory=memory
    )
    return conversation_chain


def rephrase_conversation(chat_history :dict, query:str) -> str:
    """
    Function to rephrase the question by taking considering chat history for better retrieval of information from vectorstore 
    """
    llm = AzureChatOpenAI(deployment_name="gpt-4-turbo", model_name="gpt-4-turbo")
    rephrased_chain = ConversationChain(llm= llm)    
    rephrased_query = rephrased_chain.predict(input = REPHRASE_QUES_PROMPT.format(chat_history =chat_history, query=query))

    return rephrased_query


def get_conversation_chain() -> ConversationChain:
    """
    Function to give answer using llm and have Window Buffer Memory for last three responses 
    """
    llm = AzureChatOpenAI(deployment_name="gpt-4-turbo",model_name="gpt-4-turbo")\
    
    memory = ConversationBufferWindowMemory(k=3)
    conversation_chain = ConversationChain(
        llm=llm,
        memory=memory
    )
    return conversation_chain
    
def extracted_text_from_pdf(pdf_path : str, txt_path : str):
    """
    Function to extract text from pdf and store in txt file
    """
    if not pdf_path.lower().endswith('.pdf') and not txt_path.lower().endswith('.txt'):
        raise ValueError("Invalid input: Function expect pdf and txt file path")
    text=" "

    with open(pdf_path,'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
            with open(os.path.join(txt_path, str(page_num)+".txt"),'w',encoding='utf-8') as file:
                file.write(text)

def read_files_from_folder(folder_path : str):
    """
    To read from text_folder having text_files
    """
    file_data : list = []
    for chapter_num,file_name in enumerate(os.listdir(folder_path)):
        if file_name.endswith(".txt"):
            with open(os.path.join(folder_path,file_name), 'r') as file:
                content = file.read()
                file_data.append({'metadata':f"PageNo{chapter_num +1}" ,"content":content})
    shutil.rmtree(folder_path) 
    return file_data


def data_preprocessing(uploaded_file_path: str, folder_path: str) -> list[dict]:
    """
    For data generation and preprocess for vector embeddings
    """
    extracted_text_from_pdf(uploaded_file_path, folder_path)
    file_data : list  = read_files_from_folder(folder_path)
    return file_data




