from .database import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Meeting(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False)
    location = db.Column(db.Text, nullable=True)
    minutes_fname = db.Column(db.String(500), nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'date': self.date,
            'location': self.location,
            'minutes_fname': self.minutes_fname
        }
