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

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    post = db.Column(db.String(500), nullable=False)
    image_uri = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())  

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

class PostLikes(db.Model):
    __tablename__ = "post_likes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())  

class MoodLog(db.Model):
    __tablename__ = "moods_log"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    mood_question = db.Column(db.String(500))
    mood_answer = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())      
