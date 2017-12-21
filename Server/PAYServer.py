from flask import Flask
from flask import request
import contact_pb2
import RWDict
import sqlite3

app = Flask(__name__)

# Helper method to convert a string to a Contact Type
def stringToContactType(string):
    return {
        'SPEAKER' : contact_pb2.Contact.SPEAKER,
        'VOLUNTEER' : contact_pb2.Contact.VOLUNTEER,
        'ATTENDANT' : contact_pb2.Contact.ATTENDANT
    }[string]

def lookforName(usernames,passwords):
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute('select * from users where username=? and password=?',(usernames,passwords))
    values = cursor.fetchall()
    print values
    return values



def openSql():
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (username varchar(40), password varchar(60))')


def addSql(usernames,passwords):
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (username varchar(40), password varchar(60))')
    cursor.execute('insert into users values (?,?)',(usernames,passwords))
    cursor.close()
    conn.commit()
    conn.close()
#    conn = sqlite3.connect('test.db')
#    cursor = conn.cursor()
#    cursor.execute('create table user (id varchar(20) primary key, username text not null, password text not null')



# Get current user - treat this as an RWDevCon Attendee using an app
@app.route("/currentUser")
def getCurrentUser():
    contact = contact_pb2.Contact()
    contact.first_name = "Vincent"
    contact.last_name = "Ngo"
    contact.twitter_name = "@vincentngo2"
    contact.email = "vincent@mail.com"
    contact.github_link = "github.com/vincentngo"
    contact.type = contact_pb2.Contact.ATTENDANT
    contact.imageName = "vincentngo.png"
    str = contact.SerializeToString()
    return str

# Get Speakers speaking at the conference. Loop through the predefinied array of contact dictionary, and create a Contact object, adding it to an array and serializing our Speakers object.
@app.route("/speakers")
def getSpeakers():
    contacts = []
    for contactDict in RWDict.speakers:
        contact = contact_pb2.Contact()
        contact.first_name = contactDict['first_name']
        contact.last_name = contactDict['last_name']
        contact.twitter_name = contactDict['twitter_name']
        contact.email = contactDict['email']
        contact.github_link = contactDict['github_link']
        contact.type = stringToContactType(contactDict['type'])
        contact.imageName = contactDict['imageName']
        contacts.append(contact)
    speakers = contact_pb2.Speakers()
    speakers.contacts.extend(contacts)
    return speakers.SerializeToString()

@app.route("/buy", methods=['POST'])
def buy():
    stripe_token = request.values.get("stripeToken")
    email = request.values.get("stripeEmail")
    product_id = request.values.get("product_id")
    str = product_id + stripe_token + email
    return str

@app.route("/regist",methods=['POST'])
def regist():
    username = request.values.get("username")
    password = request.values.get("password")
    
    if username != "":
        values = lookforName(username,password);
        if values:
           return "there is olready"
        else:
           addSql(username,password)
           return username
    else:
       return "-1"

@app.route("/login",methods=['POST'])
def login():
    username = request.values.get("username")
    password = request.values.get("password")
    
    if username != "":
        values = lookforName(username,password);
        print values
        if values:
           return username
        else:
           return "-2"
    else:
        return "-1"



if __name__ == "__main__":
    app.debug = True
    app.run()
