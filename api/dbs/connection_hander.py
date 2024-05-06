import os
from dotenv import load_dotenv
import pyodbc
from pymongo import MongoClient

load_dotenv()


class ConnectionHandler:
    def __init__(self):
        connection_string = os.getenv("SQL_SERVER_STRING")
        print("connection_string: ", connection_string)
        self.conn = pyodbc.connect(connection_string)
        print("ConnectionHandler init.", self.conn)

    def fetch_data(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows


def connect_to_mongodb():
    # uri = os.getenv("MONGODB_STRING")
    # database_name = os.getenv("MONGODB_DATABASE_NAME")
    uri = 'mongodb+srv://thien10a5:123123123q@mongodb-embeddings.ahdwpot.mongodb.net/'
    database_name = 'embeddings'
    print("uri: ", uri)
    print("database_name: ", database_name)
    # Chuỗi kết nối MongoDB
    client = MongoClient(uri)
    # Kết nối đến cơ sở dữ liệu
    db = client[database_name]  # Thay thế 'your_database_name' bằng tên của cơ sở dữ liệu MongoDB của bạn
    return db

db_connection = ConnectionHandler()
