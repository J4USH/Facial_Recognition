import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

"""Prototype Facial Recognition"""


"""Start of Database Code Replacement"""
path = 'FacialRecognition\ImageDataset'
images = []
classNames = []
alredy_attended = []
marked = False 

myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)
"""End of DataBase Code Replacement"""



"""Getting the Encoding of the Images"""
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList




"""Marking Attendance"""

# def markAttendance(name,alredy_attended,marked):
#     with open('Attendance.csv', 'r+') as f:
#         myDataList = f.readlines()


#         nameList = []
#         for line in myDataList:
#             entry = line.split(',')
#             nameList.append(entry[0])
#             if name not in nameList and name not in alredy_attended:
#                 print("Writing name: Dr",name)
#                 now = datetime.now()
#                 dtString = now.strftime("%m/%d/%Y,%H:%M:%S")
#                 f.writelines(f'\n{name},{dtString}')
#                 alredy_attended.append(name)
#                 marked = True
#             elif name in alredy_attended and marked:
#                 print(("ALREADY MARKED"))
#                 marked = False

"""Sending the Image from the Database of Encoding Function"""
encodeListKnown = findEncodings(images)
print(encodeListKnown)




"""Start of Video Capture"""
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_POS_FRAMES,0)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 0)
cap.set(3, 640)
cap.set(4, 480)


"""Turn the Webcam/Cam On"""
while True:
    success, img = cap.read()
    
  
    cv2.namedWindow("FacialDetection", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("FacialDetection", 700, 800)
    # imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    img_chc=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    facesCurFrame = face_recognition.face_locations(img_chc)
    encodesCurFrame = face_recognition.face_encodings(img_chc, facesCurFrame)
    """Find the faces and checking if the face is in the Database """
    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)
        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            y1, x2, y2, x1 = faceLoc
            print(faceLoc)
            """Print the face which the model has recognised"""
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, ( x1,y2 - 35,), (x2,y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, ( x1 + 6,y2 - 6 ), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            # markAttendance(name, alredy_attended,marked)
    """Pressing Q key to terminate the cam and stopping the program"""
    cv2.imshow("FacialDetection",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

