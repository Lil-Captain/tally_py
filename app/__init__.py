from flask import Flask
from app.config import Config
from app.extensions import db
from app.routes.api import api_bp
from .models import *
import pymysql
from flask_migrate import Migrate
from app.logging import setup_logger

pymysql.install_as_MySQLdb()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化logging
    setup_logger()

    db.init_app(app)

    # 初始化 migrate
    Migrate(app, db)

    app.register_blueprint(api_bp, url_prefix="/v1/api")

    return app