from dotenv import load_dotenv
import os
load_dotenv()

FLASK_DEBUG=os.environ.get("FLASK_DEBUG", False)
FLASK_DEVELOPMENT_PORT=os.environ.get("FLASK_DEVELOPMENT_PORT")
SQL_SERVER_HOST=os.environ.get("SQL_SERVER_HOST")
SQL_SERVER_USER=os.environ.get("SQL_SERVER_USER")
SQL_SERVER_PASSWORD=os.environ.get("SQL_SERVER_PASSWORD")
SQL_SERVER_DB=os.environ.get("SQL_SERVER_DB")
SQL_SERVER_URI=f'mssql+pyodbc://${SQL_SERVER_USER}:${SQL_SERVER_PASSWORD}@${SQL_SERVER_HOST}/${SQL_SERVER_DB}?driver=SQL+Server'