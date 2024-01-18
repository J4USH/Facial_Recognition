import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime



path = 'ImageDataset'
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


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList




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

encodeListKnown = findEncodings(images)
print(encodeListKnown)



cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)












while True:
    success, img = cap.read()
    
  
    cv2.namedWindow("Merge", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Merge", 700, 800)
    # imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    facesCurFrame = face_recognition.face_locations(img)
    encodesCurFrame = face_recognition.face_encodings(img, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)
        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            y1, x2, y2, x1 = faceLoc
            print(faceLoc)
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (y1, x1), (y2, x2), (0, 255, 0), 2)
            cv2.rectangle(img, ( y2 - 35,x1), (y2, x2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, ( y2 - 6 ,x1 + 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            # markAttendance(name, alredy_attended,marked)

    cv2.imshow("Merge",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
