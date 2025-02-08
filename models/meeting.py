from .database import db
from datetime import datetime

class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    minutes_url = db.Column(db.String(500), nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.isoformat(),
            'title': self.title,
            'description': self.description,
            'minutes_url': self.minutes_url
        }
