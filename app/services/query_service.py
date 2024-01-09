from langchain_openai import OpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from app.resource.response_builder import Custom
from app.services import *

class QueryService:
    def runQuery(self, query):
        llm = OpenAI(openai_api_key = OPENAI_API_KEY, temperature = 0.5, max_tokens=1000)
        docsearch = Chroma(persist_directory=VECTOR_STORE, embedding_function=embeddings)
        qa = RetrievalQA.from_chain_type(llm=llm, 
                                 chain_type="stuff",
                                 retriever=docsearch.as_retriever(),
                                 return_source_documents=False,
                                 )
        answer = qa.invoke(query)
        return Custom.jsonRes(answer,200)