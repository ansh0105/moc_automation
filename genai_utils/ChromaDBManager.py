import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict
from tqdm import tqdm
import os
moc_automation_dir_path = "/".join(os.path.abspath(__file__).split('\\')[:-2])

class ChromaDBManager:
    """
    ChromaDB class that helps to connect with chroma and initilaize sentence transformer embedding model
    It has functions to create database, create data, push data in vector database and as well as query the data from chroma.
    uses chroma==0.4.3 version 
    """
    def __init__(self, collection_name = "NewTechGen", persist_directory_name = "techdb"):
        try:
            print(os.path.join(moc_automation_dir_path, "genai_utils", persist_directory_name))
            self.client = chromadb.PersistentClient(path = os.path.join(moc_automation_dir_path, "genai_utils", persist_directory_name) )

            self.collection = self.client.get_or_create_collection(name= collection_name)
  
        except Exception as e:
            print(f"Exception raised while initializing the chroma as -- {e}")
            self.collection = None

        try:
            self.embedding_model = SentenceTransformer(os.path.join(moc_automation_dir_path,
                                                                    'genai_utils',
                                                                    'embedding_model',    
                                                                    'all_minilm_l6_v2_model'))
        except Exception as e:
            print(f"Exception raised while initializing the model as -- {e}")
            self.embedding_model = None

    def create_data(self, file_data: List[Dict]):
        document : list = list()
        metadata : list = list()
        embedding : list = list()
        ids : list = list()

        for index, data in enumerate(file_data):
            document.append(data['content'])
            embed = self.embedding_model.encode(data["content"]).tolist()
            embedding.append(embed)
            metadata.append({'source': data['metadata']})
            ids.append(str(index+1))

        return document,embedding,metadata,ids

    def push_data(self, document: list, embedding: list, metadata: list, ids: list):
        print(ids,metadata)
        try:
            self.collection.upsert(
                documents = document,
                embeddings = embedding,
                metadatas = metadata,
                ids= ids
            )
        except Exception as e:
            print(e)
        print(3)

    def query_data(self, query: str) -> dict:
        try:
            input_em = self.embedding_model.encode(query).tolist()

            result = self.collection.query(
                query_embeddings = [input_em],
                n_results=1
              
            )
            return result
        except Exception as e:
            print(f"Exception raise while quering the result as -- {e}")
            return None
        
