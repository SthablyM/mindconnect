from datetime import timezone
from db import db

class User(db.Model):
    __tablename__ = "users" 

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100))
    phone_number = db.Column(db.String(16))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(500), unique=False, nullable=False)
    created_at = db.Column(db.DateTime, default=timezone.now)
    updated_at = db.Column(db.DateTime, default=timezone.now)    