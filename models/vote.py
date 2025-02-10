from .database import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Vote(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(255), nullable=False)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'), nullable=False)
    votes_for = db.Column(db.Integer, default=0)
    votes_against = db.Column(db.Integer, default=0)
    carried = db.Column(db.Boolean, nullable=False, default=False)

    meeting = db.relationship('Meeting', backref=db.backref('votes', lazy=True))

    def to_dict(self):
        return {
            'id': str(self.id),
            'title': self.title,
            'meeting_id': self.meeting_id,
            'votes_for': self.votes_for,
            'votes_against': self.votes_against,
            'carried': self.carried
        }
