import pyrebase


# handle DataBase
firebaseConfig = {
    "apiKey": "AIzaSyBgtvYcVOMpesEzT5_tBhqjytVzFutDvuU",
    "authDomain": "minerva-v1.firebaseapp.com",
    "databaseURL": "https://minerva-v1-default-rtdb.firebaseio.com/",
    "projectId": "minerva-v1",
    "storageBucket": "minerva-v1.appspot.com",
    "messagingSenderId": "64874373634",
    "appId": "1:64874373634:web:18b8966b5a37bd98c4fd1b",
    "measurementId": "G-YW3CEWL44K",
}

firebase=pyrebase.initialize_app(firebaseConfig)
storage=firebase.storage()
database=firebase.database()
auth = firebase.auth()

def create_user(email, password):
    auth.create_user_with_email_and_password(email, password)

