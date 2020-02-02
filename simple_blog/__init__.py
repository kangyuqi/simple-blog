"""
工厂函数
"""
import os
from flask import Flask

from simple_blog.settings import config


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('simple_blog')
    app.config.from_object(config[config_name])

    return app