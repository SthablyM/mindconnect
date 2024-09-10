from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users" 

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100))
    phone_number = db.Column(db.String(16))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(500), unique=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())

    # posts = db.relationship('Post', backref='posts')  

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    post = db.Column(db.String(500), nullable=False)
    image_uri = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())  
    
    post_comments = db.relationship('PostComment', backref='posts')
    post_likes = db.relationship("PostLike", backref="posts")     


    # comments = db.relationship("PostComment", back_populates="post", lazy="dynamic")
    # likes = db.relationship("PostLike", back_populates="post", lazy="dynamic")     

class PostComment(db.Model):
    __tablename__ = "post_comments"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    comment = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now()) 

    post = db.relationship("Post", back_populates="post_comments")

class PostLike(db.Model):
    __tablename__ = "post_likes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())  

    post = db.relationship("Post", back_populates="post_likes")

class MoodLog(db.Model):
    __tablename__ = "moods_log"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    mood_question = db.Column(db.String(500))
    mood_answer = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())      
