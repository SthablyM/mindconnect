from datetime import timezone
from db import db

class PostComment(db.Model):
    __tablename__ = "post_comments"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False),
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    comment = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=timezone.now)
    updated_at = db.Column(db.DateTime, default=timezone.now)  