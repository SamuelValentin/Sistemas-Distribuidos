from flask import Flask
from flask_restx import Api, Resource

from src.server.instance import server

app, api = server.app, server.api

comps = [
    {'id': 0, 'title': 'Aula 1'},
    {'id': 1, 'title': 'Aula 2'}
]

@Api.route('/comps')
class BookList(Resource):
    def get(self, ):
        return comps