from flask import Flask
from flask_cors import CORS
def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/compiler/*": {"origins":[ "http://localhost:5173","https://apl-front-end.vercel.app"]}})

    from .controllers.compiler_controller import compiler_bp
    app.register_blueprint(compiler_bp, url_prefix="/compiler")

    return app
