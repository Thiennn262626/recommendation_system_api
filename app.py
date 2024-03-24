import os

from flask import Flask
from dotenv import load_dotenv

from api.views import blueprint

app = Flask(__name__)
app.config.from_object('config')
app.register_blueprint(blueprint=blueprint)

host = app.config.get("APP_HOST", "0.0.0.0")
port = app.config.get("FLASK_DEVELOPMENT_PORT", 8000)
debug = app.config.get('FLASK_DEBUG', False)

@app.route('/', methods=['GET'])
def hello():
    return 'port'

@app.route('/a', methods=['GET'])
def helloo():
    return port

@app.route('/b', methods=['GET'])
def hellooo():
    return os.getenv('FLASK_DEBUG')

if __name__ == '__main__':
    load_dotenv()
    app.run(host=host, port=port, debug=debug)