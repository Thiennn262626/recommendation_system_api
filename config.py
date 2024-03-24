from dotenv import load_dotenv
import os
load_dotenv()

FLASK_DEBUG=os.environ.get("FLASK_DEBUG", False)
FLASK_DEVELOPMENT_PORT=os.environ.get("FLASK_DEVELOPMENT_PORT")