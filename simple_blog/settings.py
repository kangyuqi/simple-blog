"""
使用Python类管理配置项
"""
import os


class BaseConfig(object):
    """基类"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_POST = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('Blog Admin', MAIL_USERNAME)

    BLOG_EMAIL = os.getenv('BLOG_EMAIL')
    BLOG_POST_PER_PAGE = 10
    BLOG_MANAGE_POST_PER_PAGE = 15
    BLOG_COMMENT_PER_PAGE = 15


class DevelopmentConfig(BaseConfig):
    """开发环境用"""
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:123456@localhost:3306/blog'


class TestingConfig(BaseConfig):
    """测试环境用"""
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:123456@localhost:3306/blog'


class ProductionConfig(BaseConfig):
    """生产环境用"""
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:123456@localhost:3306/blog'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}