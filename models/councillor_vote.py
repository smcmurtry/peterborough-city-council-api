from .database import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class CouncillorVote(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vote_id = db.Column(UUID(as_uuid=True), db.ForeignKey('vote.id'), nullable=False)
    councillor_id = db.Column(db.String(100), db.ForeignKey('councillor.id'), nullable=False)
    vote_cast = db.Column(db.String(20), nullable=False)  # 'yes', 'no', 'abstain'
    
    councillor = db.relationship('Councillor', backref=db.backref('councillor_votes', lazy=True))
    vote = db.relationship('Vote', backref=db.backref('councillor_votes', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'vote_id': self.vote_id,
            'councillor_id': self.councillor_id,
            'vote_cast': self.vote_cast
        }
