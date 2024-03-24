from datetime import datetime

from flask_restful import Resource, reqparse
from flask import jsonify
from connection_hander import db_connection

class UserList(Resource):
    def get(self):
        users = db_connection.fetch_data('SELECT id FROM [User]')
        return jsonify(result=users)