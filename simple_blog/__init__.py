"""
工厂函数
"""
import os
import click
from flask import Flask, render_template

from simple_blog.blueprints.admin import admin_bp
from simple_blog.blueprints.auth import auth_bp
from simple_blog.blueprints.blog import blog_bp
from simple_blog.settings import config
from simple_blog.extensions import bootstrap, db, moment, ckeditor, mail


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('simple_blog')  # Type:Flask  # 添加类型注解，开启flask相关自动补全
    app.config.from_object(config[config_name])

    register_logging(app)
    register_extensions(app)
    register_blueprints(app)
    register_shell_context(app)
    register_template_context(app)
    register_errors(app)
    register_commands(app)

    return app


def register_logging(app):
    """注册日志处理器"""
    pass


def register_extensions(app):
    """注册扩展（初始化）"""
    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)


def register_blueprints(app):
    """注册蓝图"""
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')


def register_shell_context(app):
    """注册shell上下文处理器"""
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)


def register_template_context(app):
    """注册模板上下文处理器"""
    pass


def register_errors(app):
    """注册错误处理函数"""
    @app.errorhandler(400)
    def bed_request(e):
        return render_template('errors/400.html'), 400


def register_commands(app):
    """注册自定义shell命令"""
    @app.cli.command()
    @click.option('--category', default=10, help='Quantity of categories, default is 10.')
    @click.option('--post', default=50, help='Quantity of posts, default is 50.')
    @click.option('--comment', default=500, help='Quantity of comments, default is 500.')
    def forge(category, post, comment):
        """Generate fake data."""
        from simple_blog.fakes import fake_admin, fake_categories, fake_posts, fake_comments

        db.drop_all()
        db.create_all()

        click.echo('Generating the administrator...')
        fake_admin()
        click.echo('Generating %d categories...' % category)
        fake_categories(category)
        click.echo('Generating %d posts...' % post)
        fake_posts(post)
        click.echo('Generating %d comments...' % comment)
        fake_comments(comment)
        click.echo('Done.')
