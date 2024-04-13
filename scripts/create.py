import cv2
from trainner import trainner
import json
from random import randint
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
import logging


logger = logging.getLogger(__name__)
def create():
    logger.info('Initialize add user function')
    camera = cv2.VideoCapture(0)

    model = YOLO("models/bestface.pt")
    name = input('Enter Name : ')
    while name.isdigit():
        print('enter only alpha')
        name = input('Enter Name : ')

    Id=randint(0,100)
    print(Id)
    itr = 1

    while 1:

        _, image = camera.read()

        grayImage = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

        result = model.predict(image ,max_det=1)
        for r in result:
            annotator = Annotator(image)
            boxes = r.boxes
            for box in boxes:
                b = box.xyxy[0]
                c = box.cls
                annotator.box_label(b, model.names[int(c)], 3)
                x, y, w, h= int(b[0]),int(b[1]),int(b[2]),int(b[3])
                cv2.rectangle(image, (x,y), (w,h), (100,100,0), 2)

                cv2.imwrite('dataset/User.' + str(Id) + '.' + str(itr) + '.jpg', grayImage[:y+h,:x+w ])

        itr += 1

        if itr == 61:
            break
        
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break

        cv2.imshow('Frame',image)
    camera.release()
    cv2.destroyAllWindows()
    logger.info('Preparing to add user')
    with open("ymlandjson_Files/users.json") as json_file:
        data = json.load(json_file)

    username = {
                'name':name
            }
    data[Id] = username
    logger.info('Adding user')
    with open("ymlandjson_Files/users.json", "w") as file:
        json.dump(data, file,indent = 4)

    path = 'dataset'
    logger.info(f'User {name} added succesfully')  
    trainner()