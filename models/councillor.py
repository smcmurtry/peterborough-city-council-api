from .database import db

class Councillor(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    ward = db.Column(db.String(50), nullable=True)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'ward': self.ward,
            'title': self.title,
            'start_date': self.start_date,
            'end_date': self.end_date,
        }
