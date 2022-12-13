import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

#firebase admin sdk
cred = credentials.Certificate("theproject\project-d4bf4-firebase-adminsdk-7esok-6ce306916e.json")
default_app = firebase_admin.initialize_app(cred)

#pyrebase sdk
config = {
    'apiKey': "AIzaSyDr4jO2Gp7j0hsx5VLHDtdObBZp7XemTOs",
    'authDomain': "project-d4bf4.firebaseapp.com",
    'databaseURL': "https://project-d4bf4-default-rtdb.firebaseio.com",
    'projectId': "project-d4bf4",
    'storageBucket': "project-d4bf4.appspot.com",
    'messagingSenderId': "145308609557",
    'appId': "1:145308609557:web:f01d105775ec058187721c",
    'measurementId': "G-7BENWP5SS7" }

firebase = pyrebase.initialize_app(config)

db = firebase.database()
pyreauth = firebase.auth()
pyrestorage = firebase.storage()

#Create function with pyreauth + adding user model to db
def firebaseacc(email, passw, name, id,DocCount, role):
    user = pyreauth.create_user_with_email_and_password(email, passw)
    data = {'name': name, 'id': id, 'DocCount': DocCount, 'role': role}
    db.child(user["localId"]).set(data)
    return user

#login function
def firebaseLoginAuth(email, passw):
    try:
        user = pyreauth.sign_in_with_email_and_password(email,passw)
        print("Success")
        return (user)
    except:
        print("Email already exists")

#saving file in cloud while returning the url
def firebaseStoreInCloud(local, cloud, user):
    try:
        x = user["localId"] +'/' + cloud
        pyrestorage.child(x).put(local)
        y = (pyrestorage.child(x).get_url(user))
        #db.child(user["localId"). set({''})

    except:
        print("failed")

#Updating model value in db
def firebaseupdateval(user, key, val):
    db.child(user["localId"]).update({key : val})

# User deleting document link in rtdb
def firebasedeletedoc(user,cloud):
    db.child(user["localId"]).child(cloud).remove()


def firebasedeleteacc(user):
    auth.delete_user(user["localId"])
    db.child(user["localId"]).remove()


#USE NECESSARY TO CHECK:
user = firebaseacc ("rafidhasan121@gmail.com", "12345678", "Rafid", 1, 0, "Manager")
#user = firebaseLoginAuth("rafidhasan121@gmail.com","12345678")
#firebasedeletedoc(user, "name")
#firebaseupdateval(user, "name", "Refid")
#user = firebaseLoginAuth("syeda.nafisa@northsouth.edu","123456")
url = firebaseStoreInCloud("Files\Test.txt", "Dababy.txt", user)
firebasedeleteacc(user)
