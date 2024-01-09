from flask import Blueprint, request, Response
from app.services.embedding_service import EmbeddingService

embedding = Blueprint('embedding', __name__)
embeddingService = EmbeddingService()

@embedding.route('/create-embedding', methods=['POST'])
def index():
    files = request.files
    return embeddingService.createEmbeddings(files=files)


    
