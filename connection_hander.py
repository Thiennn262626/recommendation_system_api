import os
from dotenv import load_dotenv
import pyodbc
load_dotenv()

class ConnectionHandler:
    def __init__(self):
        # connection_string = os.environ.get("SQL_SERVER_STRING")
        connection_string = os.getenv("SQL_SERVER_STRING")
        self.conn = pyodbc.connect(connection_string)

    def fetch_data(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        id_list = [row[0] for row in rows]
        return id_list

db_connection = ConnectionHandler()