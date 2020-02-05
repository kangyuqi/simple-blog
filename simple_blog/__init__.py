"""
工厂函数
"""
import os
from flask import Flask

from simple_blog.settings import config
from simple_blog.extensions import bootstrap, db, moment, ckeditor, mail


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('simple_blog')
    app.config.from_object(config[config_name])

    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)

    return app