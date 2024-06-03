from flask import Flask, request, jsonify
from database import *


app = Flask(__name__)


# Configuring the database with flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "i_am_ironman"  

# Intitiating the database
init_db(app)


# /identify endpoint
@app.route('/identify', methods=['POST'])
def identify():

    # data from json payload
    payload = request.get_json()
    email = payload.get('email')
    phoneNumer = payload.get('phoneNumber')

    # checking for existing contacts with same data
    emailMatch = get_contact_by_email(email=email)

    phoneNumerMatch = get_contact_by_phoneNumber(phoneNumber=phoneNumer)

    # If no match, then create new user

    if emailMatch is None and phoneNumerMatch is None:
        newcontact = create_contact(email=email, phoneNumber=phoneNumer)

        return jsonify({
            "contact" : {
            "primaryContatctId": newcontact.id,
            "emails": [newcontact.email], 
            "phoneNumbers": [newcontact.phoneNumber], 
            "secondaryContactIds": [] }
        })
    
    elif emailMatch is not None and phoneNumerMatch is not None:
        # Find which contact has created first
        if emailMatch.id == phoneNumerMatch.id:
            primaryContact = emailMatch

        # check id orders and update linkId and precendence
        elif emailMatch.id < phoneNumerMatch.id:
            primaryContact = emailMatch
            update_contact(phoneNumerMatch, primaryContact.id)


        elif emailMatch.id > phoneNumerMatch.id:
            primaryContact = phoneNumerMatch
            update_contact(emailMatch, primaryContact.id)

    elif emailMatch is not None:
        newcontact = create_contact(email=email, phoneNumber=phoneNumer)
        primaryContact = emailMatch
        update_contact(newcontact, primaryContact.id)
    
    elif phoneNumerMatch is  not None:
        newcontact = create_contact(email=email, phoneNumber=phoneNumer)
        primaryContact = phoneNumerMatch
        update_contact(newcontact, primaryContact.id)
    

    # fetches all secondary data
    secondaryContactData = fetch_details(primaryContact)

    return jsonify({
            "contact" : {
            "primaryContatctId": primaryContact.id,
            "emails": [primaryContact.email] + secondaryContactData['email'], 
            "phoneNumbers": [primaryContact.phoneNumber] + secondaryContactData['phoneNumbers'], 
            "secondaryContactIds": secondaryContactData['secondaryIds'] }
        })



if __name__ == '__main__':
    app.run(debug=True)
