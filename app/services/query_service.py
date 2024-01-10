from langchain_openai import OpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA, RetrievalQAWithSourcesChain
from app.resource.response_builder import Custom
from app.services import *
from langchain_community.agent_toolkits import create_openapi_agent


# Cite sources
def process_llm_response(llm_response):
    result = llm_response['result']
    if len(llm_response["source_documents"])==0:
        return "Can't find answer to this from current context",[]
    
    documents = llm_response["source_documents"]
    unique_pages_per_source = {}
    for document in documents:
        source = document.metadata['source'].split('/')[-1]
        page = document.metadata.get('page')  
        if source not in unique_pages_per_source:
            unique_pages_per_source[source] = set()
        if page is not None:
            unique_pages_per_source[source].add(page)
    # unique_pages_per_source_json_serialized = {k: list(v) for k, v in unique_pages_per_source.items()}
    unique_pages_per_source_json_serialized = {k: ', '.join(map(str, sorted(v))) for k, v in unique_pages_per_source.items()}
    return result, unique_pages_per_source_json_serialized

class QueryService:
    def runQuery(self, query):
        llm = OpenAI(openai_api_key = OPENAI_API_KEY, temperature = 0, max_tokens=500)
        docsearch = Chroma(persist_directory=VECTOR_STORE, embedding_function=embeddings)
        qa = RetrievalQA.from_chain_type(llm=llm, 
                                 chain_type="stuff",
                                 retriever=docsearch.as_retriever(),
                                 return_source_documents=True,
                                 verbose=True
                                 )
        llm_response = qa(query)
        answer, sources = process_llm_response(llm_response)
        print(f"sources: {sources}")
        return Custom.jsonRes(status=200,message=answer, sources=sources)