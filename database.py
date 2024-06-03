import secrets
from models import db, Contacts
from datetime import datetime, timedelta
from flask import jsonify

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

# User data functions
def create_contact(email, phoneNumber, linkPrecedence = "Primary"):
    contact = Contacts(
        email=email, 
        phoneNumber = phoneNumber,
        updatedAt = datetime.now(),
        createdAt = datetime.now(),
        linkPrecedence = linkPrecedence
        )
    db.session.add(contact)
    db.session.commit()
    return contact

def get_contact_by_email(email):
    return Contacts.query.filter_by(email=email).first()

def get_contact_by_phoneNumber(phoneNumber):
    return Contacts.query.filter_by(phoneNumber=phoneNumber).first()

def update_contact(contact, linkId):
    contact.linkId = linkId
    contact.updatedAt = datetime.now()
    contact.linkPrecedence = "Secondary"
    db.session.commit()


def fetch_details(contact):

    secondaryContacts = Contacts.query.filter_by(linkId = contact.id).all()
    secondaryData = {
        'email' : [],
        'phoneNumbers' : [],
        'secondaryIds' : []
    }

    for contacts in secondaryContacts:
        secondaryData['email'].append(contacts.email)
        secondaryData['phoneNumbers'].append(contacts.phoneNumber)
        secondaryData['secondaryIds'].append(contacts.id)
    
    return secondaryData
