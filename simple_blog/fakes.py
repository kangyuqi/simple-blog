"""
虚拟数据
"""
import random

from faker import Faker
from sqlalchemy.exc import IntegrityError

from simple_blog.models import Admin, Category, Post, Comment
from simple_blog.extensions import db

fake = Faker()


def fake_admin():
    admin = Admin(
        username='admin',
        blog_title='simple_blog',
        blog_sub_title="No, I'm the real thing.",
        name='Aaron Kang',
        about='Who are you?'
    )
    db.session.add(admin)
    db.session.commit()


def fake_categories(count=10):
    category = Category(name='Default')
    db.session.add(category)
    for _ in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:  # 如果随机产生的分类名和已创建的重名，就会导致数据库出错，此处捕获
            db.session.rollback()


def fake_posts(count=50):
    for _ in range(count):
        post = Post(
            title=fake.sentence(),
            body=fake.text(2000),
            category=Category.query.get(random.randint(1, Category.query.count())),  # 随机获取分类
            timestamp=fake.date_time_this_year()
        )
        db.session.add(post)
    db.session.commit()


def fake_comments(count=500):
    """生成虚拟评论"""
    for i in range(count):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

    salt = int(count * 0.1)
    for i in range(salt):
        # 未审核评论
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

        # 管理员发表的评论
        comment = Comment(
            author='Aaron Kang',
            email='aaron@example.com',
            site='example.com',
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            from_admin=True,
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

    db.session.commit()

    # 回复
    for i in range(salt):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            replied=Comment.query.get(random.randint(1, Comment.query.count())),
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

    db.session.commit()