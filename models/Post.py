from datetime import timezone
from db import db

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False),
    post = db.Column(db.String(500), nullable=False)
    image_uri = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=timezone.now)
    updated_at = db.Column(db.DateTime, default=timezone.now)  

    comments = db.relationship("PostComment", back_populates="post", lazy="dynamic")
    likes = db.relationship("PostLike", back_populates="post", lazy="dynamic")