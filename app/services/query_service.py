from langchain_openai import OpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA, RetrievalQAWithSourcesChain
from app.resource.response_builder import Custom
from app.services import *
from langchain_community.agent_toolkits import create_openapi_agent


# Cite sources
def process_llm_response(llm_response):
    sources = set()
    result = llm_response['result']
    print('\n\nSources:')
    for source in llm_response["source_documents"]:
        filepath = source.metadata['source']
        filename = filepath.split('/')[-1]
        pageno = source.metadata['page']
        sources.add(f"{filename}/{pageno}")
    combined_sources=  ','.join(sorted(sources))
    return result, combined_sources

class QueryService:
    def runQuery(self, query):
        llm = OpenAI(openai_api_key = OPENAI_API_KEY, temperature = 0, max_tokens=1000)
        docsearch = Chroma(persist_directory=VECTOR_STORE, embedding_function=embeddings)
        qa = RetrievalQA.from_chain_type(llm=llm, 
                                 chain_type="stuff",
                                 retriever=docsearch.as_retriever(),
                                 return_source_documents=True,
                                 verbose=True
                                 )
        print(qa.combine_documents_chain.llm_chain.prompt.template)

        # answer = qa.invoke(query)
        llm_response = qa(query)
        print(llm_response)
        answer, sources = process_llm_response(llm_response)
        return Custom.jsonRes(status=200,message=answer, sources=sources)