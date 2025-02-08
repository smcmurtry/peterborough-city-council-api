from .database import db

class Councillor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ward = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'ward': self.ward,
            'email': self.email
        }
