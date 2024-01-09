from flask import Blueprint, request, Response
from app.services.embedding_service import EmbeddingService

embedding = Blueprint('embedding', __name__)
embeddingService = EmbeddingService()

@embedding.route('/create-embedding', methods=['POST'])
def index():
    uploaded_files = request.files.getlist("files[]")
    return embeddingService.createEmbeddings(uploaded_files=uploaded_files)


    
