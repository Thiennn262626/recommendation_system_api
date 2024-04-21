from flask import Flask

from api.views import blueprint

app = Flask(__name__)
app.config.from_object('config')
app.register_blueprint(blueprint=blueprint)

host = app.config.get("APP_HOST", "0.0.0.0")
port = app.config.get("FLASK_DEVELOPMENT_PORT", 8000)
debug = app.config.get('FLASK_DEBUG', False)

@app.route('/')
def index():
    return {'message': 'Welcome to the API'}

if __name__ == '__main__':
    app.run(host=host, port=port, debug=debug)