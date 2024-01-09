from flask import Response, jsonify

class Custom:
    def jsonRes(message, status):
        return Response(response=jsonify({'message':message}).data,status=status,headers={'Content-Type': 'application/json'})