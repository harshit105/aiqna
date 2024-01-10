from flask import Response, jsonify

class Custom:
    def jsonRes(status, **kwargs):
        return Response(response=jsonify(kwargs).data, status=status, headers={'Content-Type': 'application/json'})