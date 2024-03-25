from datetime import datetime

from flask_restful import Resource, reqparse
from flask import jsonify
from connection_hander import db_connection

class UserList(Resource):
    def get(self):
        users = db_connection.fetch_data('SELECT id, id_account FROM [User]')
        json_array = [{'id': result[0], 'id_account': result[1]} for result in users]
        return jsonify(result=json_array)