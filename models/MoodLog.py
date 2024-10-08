from datetime import timezone
from db import db

class MoodLog(db.Model):
    __tablename__ = "moods_log"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False),
    mood_question = db.Column(db.String(500))
    mood_answer = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=timezone.now)
    updated_at = db.Column(db.DateTime, default=timezone.now)  