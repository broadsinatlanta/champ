from champ import db
from datetime import datetime


class Feedback(db.Model):
    """
    Feedback table model.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    posted_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    sentiment = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    positive = db.Column(db.String(50), nullable=False)
    negative = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return "Name: %s, Message: %s\n" % (self.name, self.message)

    def save(self):
        """
        Method to add & save change itself (as a Feedback object) to the champ
        db.
        """

        db.session.add(self)
        db.session.commit()
