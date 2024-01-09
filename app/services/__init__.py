import os
from langchain_openai import OpenAIEmbeddings

UPLOAD_FOLDER = 'app/meta/uploads'
VECTOR_STORE = 'app/meta/chromadb'
OPENAI_API_KEY = os.environ.get("OPEN_API_KEY")
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, model="text-embedding-ada-002")

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)