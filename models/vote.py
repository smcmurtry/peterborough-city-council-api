from .database import db

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    councillor_id = db.Column(db.Integer, db.ForeignKey('councillor.id'), nullable=False)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'), nullable=False)
    vote_cast = db.Column(db.String(20), nullable=False)  # 'yes', 'no', 'abstain'
    
    councillor = db.relationship('Councillor', backref=db.backref('votes', lazy=True))
    meeting = db.relationship('Meeting', backref=db.backref('votes', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'councillor_id': self.councillor_id,
            'meeting_id': self.meeting_id,
            'vote_cast': self.vote_cast
        }
