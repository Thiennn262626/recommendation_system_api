# from datetime import datetime
# from sqlalchemy.engine import URL
# from sqlalchemy import create_engine
# from sqlalchemy.pool import QueuePool
# import pandas as pd
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

#     def insert_data(self, df, tablename):
#         df.to_sql(tablename, if_exists='append', index=False, con=self.db_connection)
#
#     def execute_query(self, query):
#         self.db_connection.execute(query)
#
#     def __del__(self):
#         try:
#             self.db_connection.close()
#         except:
#             None

db_connection = ConnectionHandler()