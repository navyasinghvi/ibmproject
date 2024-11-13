import pickle
import cv2
import os
import face_recognition
import cvzone
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime
#using firebase
cred = credentials.Certificate("service key.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://pbl-facerecognition-default-rtdb.firebaseio.com/",
    'storageBucket':"pbl-facerecognition.appspot.com"
})
bucket=storage.bucket()
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
imgback = cv2.imread('giu/background.jpg')

#importing images to a list
folderPath = 'giu/extra'
modepathlist = os.listdir(folderPath)
imageModelist = []
for path in modepathlist:
    imageModelist.append(cv2.imread(os.path.join(folderPath, path)))

#load the encoding file
print("loading encode file")
file=open("encodefile.p",'rb')
encodelistknownids=pickle.load(file)
file.close()
encodelistknown,studentid=encodelistknownids
#print(studentid)
print("encode file loaded")


modetype=0
counter=0
id=-1
imgstudent=[]
while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    img_resized = cv2.resize(img, (430, 280))
    imgback[155:155 + 280, 27:27 + 430] = img_resized
    resized_image = cv2.resize(imageModelist[modetype], (275, 425))
    imgback[27:27 + 425, 535:535 + 275] = resized_image
    if facesCurFrame:
        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodelistknown, encodeFace)
            faceDis = face_recognition.face_distance(encodelistknown, encodeFace)
            # print(faceDis)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                y1, x2, y2, x1 = faceLoc

                id=studentid[matchIndex]

                if counter==0:
                    counter=1
                    modetype=1
        if counter!=0:
            if counter ==1:
                #get the data
               studentinfo= db.reference(f'students/{id}').get()
               print(studentinfo)
                #get image from storage
               blob=bucket.get_blob(f'images attendance/{id}.jpg')
               array=np.frombuffer(blob.download_as_string(),np.uint8)
               imgstudent=cv2.imdecode(array,cv2.COLOR_BGRA2BGR)
                #update the data
               datetimeobject=datetime.strptime(studentinfo['last_attendance_time'],
                                               "%d-%m-%Y %H:%M:%S")
               secondselapsed=(datetime.now()-datetimeobject).total_seconds()
               if secondselapsed > 30:

                   ref=db.reference(f'students/{id}')
                   studentinfo['total_attendance']+=1
                   ref.child('total_attendance').set(studentinfo['total_attendance'])
                   ref.child('last_attendance_time').set(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
               else:
                   modetype=3
                   counter=0
                   resized_image = cv2.resize(imageModelist[modetype], (275, 425))
                   imgback[27:27 + 425, 535:535 + 275] = resized_image


            if modetype!=3:

                if 10<counter<20:
                    modetype=2
                resized_image = cv2.resize(imageModelist[modetype], (275, 425))
                imgback[27:27 + 425, 535:535 + 275] = resized_image
                if counter <= 10:

                    cv2.putText(imgback,str(studentinfo['name']),(610,90),
                            cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,0),1)
                    cv2.putText(imgback, str(studentinfo['dept']), (653, 290),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (1, 1, 1),1)
                    cv2.putText(imgback, str(id), (655, 250),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)
                    cv2.putText(imgback, str(studentinfo['total_attendance']), (593, 370),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)
                    cv2.putText(imgback, str(studentinfo['year']), (660, 370),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)
                    cv2.putText(imgback, str(studentinfo['start_year']), (710, 370),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)
                    img_resiz = cv2.resize(imgstudent, (134, 124))
                    imgback[97:97 + 124, 600:600 + 134] = img_resiz
                counter+=1

                if counter>=20:
                    counter=0
                    modetype=0
                    studentinfo=[]
                    imgstudent=[]
                    resized_image = cv2.resize(imageModelist[modetype], (275, 425))
                    imgback[27:27 + 425, 535:535 + 275] = resized_image
    else:
        modetype=0
        counter=0


    cv2.imshow("Image", imgback)
    cv2.waitKey(1)