import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("service key.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://pbl-facerecognition-default-rtdb.firebaseio.com/",
    'storageBucket':"pbl-facerecognition.appspot.com"
})

#importing images
folderPath = 'images attendance'
pathlist = os.listdir(folderPath)
imglist = []
studentid=[]
for path in pathlist:
    imglist.append(cv2.imread(os.path.join(folderPath, path)))
    studentid.append(os.path.splitext(path)[0])

    fileName= f'{folderPath}/{path}'
    bucket=storage.bucket()
    blob=bucket.blob(fileName)
    blob.upload_from_filename(fileName)

print(studentid)


def findencodings(imageslist) :
    encodeList = []
    for img in imageslist:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
print("encoding started...")
encodelistknown=findencodings(imglist)
encodelistknownids=[encodelistknown,studentid]
print("encoding complete")

file = open("encodefile.p",'wb')
pickle.dump(encodelistknownids,file)
file.close()
print("file saved")