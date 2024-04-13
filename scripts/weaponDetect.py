import cv2 as cv
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
model = YOLO("models/weapondetection.pt")
from playsounds import playsound
import threading

def weapondetecter():

    camera = cv.VideoCapture(0)
    while True:
        res, frame = camera.read()
        if not res:
            break
        else:
            result = model.predict(frame)
            for r in result:
                annotator = Annotator(frame)
                boxes = r.boxes
                for box in boxes:
                    b = box.xyxy[0]
                    c = box.cls
                    annotator.box_label(b, model.names[int(c)], 3)
                    
                    alarm_thread = threading.Thread(target=playsound, args=("alarm3.wav",))
                    alarm_thread.start()
        cv.imshow('Image', frame)
        if cv.waitKey(20) & 0xFF == ord('q'):
            break
    camera.release()
    cv.destroyAllWindows()

# weapondetecter()