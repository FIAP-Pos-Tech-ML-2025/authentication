from flask import Flask
from src.config import settings
from src.api.routes import auth_bp
from src.utils import get_logger

def create_app():
    app = Flask(settings.APP_NAME)
    logger = get_logger()
    app.register_blueprint(auth_bp)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)