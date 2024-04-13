import cv2 as cv
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
# import mediapipe as mp
import numpy as np
import os
from scripts.send_emails import send_emails
# from send_emails import send_emails
from random import randint
import random
import datetime
import json
# import pyrebase
import threading
from playsound import playsound


model = YOLO("models/best_me.pt")
model2 = YOLO("models/bestface.pt")
model3= YOLO("models/yolov8n.pt")

# load recognizer and users
# recognizer = cv.face.LBPHFaceRecognizer_create()
# recognizer.read('ymlandjson_Files/trainneruser.yml')

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

# firebase=pyrebase.initialize_app(firebaseConfig)
# storage=firebase.storage()
# database=firebase.database()
# auth = firebase.auth()

# # open users json file and retrieve names
with open('ymlandjson_Files/users.json') as jsonFile:
    users = json.load(jsonFile)

def faceRecognation(frame):
    global faceId
    global name
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    height, width = frame.shape[:2]
    userList = []
    result = model2.predict(frame)
    for r in result:
        annotator = Annotator(frame)
        boxes = r.boxes
        for box in boxes:
            b = box.xyxy[0]
            c = box.cls
            x, y, w, h = int(b[0]), int(b[1]), int(b[2]), int(b[3])
            cv.rectangle(frame, (x, y), (w, h), (100, 0, 100), 2)
            # faceId, percentage = recognizer.predict(gray[y:y + h, x:x + w])
            # faceId=str(faceId)
            # if percentage < 50:
            #     if faceId in users:
            #         userList.append(faceId)
            #         name = users[faceId]['name']+' '+users[faceId]['mode']
            #     else:
            #         name = 'Unknown'
            # else:
            #     name = 'Unknown'
            cv.putText(frame, (x, y), cv.FONT_HERSHEY_SIMPLEX, 1, (50, 255,), 2)

def frameProcess(frame):
    alarm_thread = threading.Thread(target=playsound, args=("alarm3.wav",))
    upload_photo_thread = threading.Thread(target=uploadphoto)

    face_thread = threading.Thread(target=faceRecognation(frame))    
    print(users[faceId]['mode'])
    print(type(users[faceId]['mode']))
    if users[faceId]['mode'] != 'Allowed' or name == 'Unknown' :
        result = model.predict(frame, classes=[1])
        annotator = Annotator(frame)
        for r in result:
            boxes = r.boxes
            for box in boxes:
                b = box.xyxy[0]
                c = box.cls
                x, y, w, h = int(b[0]), int(b[1]), int(b[2]), int(b[3])

                annotator.box_label(b, model.names[int(c)], 3)
                cv.imwrite("screenShot3.jpg", frame)
                MailThread = threading.Thread(target=send_emails)
                alarm_thread.start()
                upload_photo_thread.start()
                MailThread.start()
    face_thread.start()

    return frame




def uploadphoto():
    data={
        'name':"unkown",
        'date':str(datetime.datetime.now())
    }
    Id = random.randrange(1, 9999, 5)
    # database.child("Real-time Abnormal Behavior Detectopm").child(f"unknown{Id}").update(data)
    # storage.child("Real-time Abnormal Behavior Detectopm").child(f"unknown{Id}.jpg").put("screenShot3.jpg")

# def create_user(email, password):
#     # auth.create_user_with_email_and_password(email, password)