from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime(), default=db.func.now())
    
    def get_dict(self):
        return {
            "id": self.id,
            "message": self.message,
            "date": self.date
        }