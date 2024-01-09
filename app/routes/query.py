from flask import Blueprint, request, Response
from app.services.query_service import QueryService

query = Blueprint('query', __name__)
queryService = QueryService()

@query.route('/run-query', methods=['POST'])
def index():
    query = request.get_json()["query"]
    return queryService.runQuery(query=query)


    
