from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from app.resource.response_builder import Custom
from langchain_community.vectorstores import Chroma
import os
import uuid
from app.services import *

seen_ids = set()

class EmbeddingService:
    
    def createEmbeddings(self,uploaded_files):
        print(uploaded_files)
        for file in uploaded_files:
            print(file.content_type)
            if file.filename == '':
                return Custom.jsonRes(status=400,message='No file selected for uploading')
            
            # save file locally
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            documents = []
            if file.content_type=="application/pdf":
                loader=PyPDFLoader(file_path=filepath)
                data = loader.load()
                text_splitter = RecursiveCharacterTextSplitter(separators=['\n\n','\n','.',','], chunk_size=1500)
                documents = text_splitter.split_documents(data)

            elif file.content_type=="text/csv":
                loader = CSVLoader(file_path=filepath)
                data = loader.load()
                text_splitter = RecursiveCharacterTextSplitter(separators=['\n'], chunk_size=1500)
                documents = text_splitter.split_documents(data)
            
            elif file.content_type=="text/plain":
                loader = TextLoader(file_path=filepath)
                data = loader.load()
                text_splitter = RecursiveCharacterTextSplitter(separators=['\n\n','\n','.',','], chunk_size=1500)
                documents = text_splitter.split_documents(data)

            else:
                return Custom.jsonRes(status=400,message='Unsuported file type')
            

            # Create a list of unique ids for each document based on the content
            ids = [str(uuid.uuid5(uuid.NAMESPACE_DNS, doc.page_content)) for doc in documents]
            unique_ids = list(set(ids))
            # Ensure that only docs that correspond to unique ids are kept and that only one of the duplicate ids is kept
            unique_docs = [doc for doc, id in zip(documents, ids) if id not in seen_ids and (seen_ids.add(id) or True)]      
            if(len(unique_docs)>0):
                Chroma.from_documents(documents=unique_docs, ids=unique_ids, embedding=embeddings, persist_directory=VECTOR_STORE)
        
        # Once vector embedding is created remove file from local
        os.remove(filepath)
        return Custom.jsonRes(status=200,message='Files successfully processed')
