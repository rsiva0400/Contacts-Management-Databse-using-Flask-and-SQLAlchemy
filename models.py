from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

db = SQLAlchemy()

# Creating a SQLAlchemy database Calss
class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phoneNumber = db.Column(db.String(100))
    email = db.Column(db.String(100))
    linkId = db.Column(db.Integer)
    linkPrecedence = db.Column(db.String(100))
    createdAt = db.Column(db.DateTime, nullable=False)
    updatedAt = db.Column(db.DateTime, nullable=False)
    deletedAt = db.Column(db.DateTime)
