"""
模型
"""
from datetime import datetime

from simple_blog.extensions import db


class Admin(db.Model):
    """管理员用"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    blog_title = db.Column(db.String(60))
    blog_sub_title = db.Column(db.String(100))
    name = db.Column(db.String(30))
    about = db.Column(db.Text)


class Category(db.Model):
    """文章分类"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)

    posts = db.relationship('Post', back_populates='category')  # 分类和文章之间是一对多的关系


class Post(db.Model):
    """文章"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    body = db.Column(db.Text)
    timestamp = db.Column(db.Datetime, default=datetime.utcnow)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', back_populates='posts')

    comments = db.relationship('Comment', backref='post', cascade='all.delete-orphan')  # 文章和评论之间是一对多双向关系，这里做了级联删除


class Comment(db.Model):
    """评论"""
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30))
    email = db.Column(db.String(254))
    site = db.Column(db.String(255))
    body = db.Column(db.Text)
    from_admin = db.Column(db.Boolean, default=False)
    reviewed = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.Datetime, default=datetime.utcnow, index=True)

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', back_populates='comments')

    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])  # 关系两侧都在统一模型中，remote_side指定远程侧
    replies = db.relationship('Comment', backref='replied', cascade='all')  # 当付评论被删除时，所有的子评论也随之删除
