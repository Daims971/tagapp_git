from flask_sqlalchemy import SQLAlchemy
import logging as lg

from .views import app

# Create database connection object
db = SQLAlchemy(app)

# class Content(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    # description = db.Column(db.String(200), nullable=False)
    # gender = db.Column(db.Integer(), nullable=False)

    # def __init__(self, description, gender):
        # self.description = description
        # self.gender = gender

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.String(300), nullable=False)

    def __init__(self, title, body):
        self.title = title
        self.body = body

# db.create_all()

def init_db():
    db.drop_all()
    db.create_all()
    db.session.add(Content("This is Title 1", "This is Body 1"))
    db.session.add(Content("This is Title 2", "This is Body 2"))
    db.session.commit()
    lg.warning('Database initialized!')