import cv2 as cv
import json
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
import threading
from playsound import playsound
import logging


logger = logging.getLogger(__name__)

camera = cv.VideoCapture(0)
model = YOLO("models/bestface.pt")
model2 = YOLO("models/best_me.pt")
weapon = YOLO("models/weapondetection.pt")

# Create LBPH face recognizer
recognizer = cv.face.LBPHFaceRecognizer_create()
recognizer.read('ymlandjson_Files/trainneruser.yml')

#open users json file and retrieve names
with open('ymlandjson_Files/users.json') as jsonFile:
    users = json.load(jsonFile)
userList = []


def live_detection():

    camera = cv.VideoCapture(0)
    while True:
        res, frame = camera.read()
        if not res:
            break
        else:
            # detect weapon
            result = weapon.predict(frame)
            for r in result:
                annotator = Annotator(frame)
                boxes = r.boxes
                for box in boxes:
                    b = box.xyxy[0]
                    c = box.cls
                    # annotator.box_label(b, model.names[int(c)], 3)
                    
                    alarm_thread = threading.Thread(target=playsound, args=("alarm3.wav",))
                    alarm_thread.start()

            result = model2.predict(frame)
            for r in result:
                annotator = Annotator(frame)
                boxes = r.boxes
                for box in boxes:
                    b = box.xyxy[0]
                    c = box.cls
                    annotator.box_label(b, model2.names[int(c)], 3)
                    logger.info(f'A {model2.names[int(c)]} has been detected within the premise')
            #detect face
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

            height, width = frame.shape[:2]
            result = model.predict(frame)
            for r in result:
                annotator = Annotator(frame)
                boxes = r.boxes
                for box in boxes:
                    b = box.xyxy[0]
                    c = box.cls
                    x, y, w, h = int(b[0]), int(b[1]), int(b[2]), int(b[3])
                    # cv.rectangle(frame, (x,y), (w, h), (100,0,100), 2)
                    cv.rectangle(frame, (x, y), (x+w, y+h), (100, 0, 100), 2)
                    faceId, mismatch = recognizer.predict(gray[y:y+h, x:x+w])
                    faceId=str(faceId)
                    if mismatch < 50  :
                        if faceId in users :
                            userList.append(faceId)
                            faceId = users[str(faceId)]['name'] + " " + users[str(faceId)]['mode']
                            name = users[str(faceId)]['name']
                            logger.info(f'{name} within premise')
                        else:
                            logger.info('unknown person within premise')
                            faceId = 'Unknown'
                    else:
                        faceId = 'Unknown'
                        logger.info('unknown person within premise')
                    cv.putText(frame, str(faceId), (x,y),cv.FONT_HERSHEY_SIMPLEX, 1, (50,255,),2)

        cv.imshow('Image', frame)
        if cv.waitKey(20) & 0xFF == ord('q'):
            break
    camera.release()
    cv.destroyAllWindows()