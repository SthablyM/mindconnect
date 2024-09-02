from datetime import timezone
from db import db

class PostLikes(db.Model):
    __tablename__ = "post_likes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False),
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=timezone.now)
    updated_at = db.Column(db.DateTime, default=timezone.now)  