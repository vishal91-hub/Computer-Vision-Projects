import os
import pickle
import numpy as np
import cv2
import face_recognition
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import numpy as np
from datetime import datetime
import pandas as pd

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
   'databaseURL': "https://faceattendance-192c4-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendance-192c4.appspot.com"""
})

bucket = storage.bucket()

cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/background.png')
#write the attenance in excel sheet also
def write_to_excel(name):
    # Get current date and time
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create DataFrame with person's details
    data = {'Name': [name],
            'Date': [current_datetime]}
    df = pd.DataFrame(data)

    # Write DataFrame to Excel file
    with pd.ExcelWriter('attendance.xlsx', mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
        df.to_excel(writer, index=False)




# Importing the mode images into a list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
# print(len(imgModeList))

# Load the encoding file
print("Loading Encode File ...")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
knownencodinglist, employeelist = encodeListKnownWithIds
# print(studentIds)
print("Encode File Loaded")

modeType = 0
counter = 0
id = -1
imgEmployee = []

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(knownencodinglist, encodeFace)
            faceDis = face_recognition.face_distance(knownencodinglist, encodeFace)
            # print("matches", matches)
            # print("faceDis", faceDis)

            matchIndex = np.argmin(faceDis)
            # print("Match Index", matchIndex)

            if matches[matchIndex]:
                # print("Known Face Detected")
                # print(employeelist[matchIndex])
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = (55 + x1, 162 + y1, 55 + x2, 162 + y2)  # Define the bounding box as (x1, y1, x2, y2)
                color = (0, 255, 0)  # Define the color as green

                # Draw the rectangle on the background image
                cv2.rectangle(imgBackground, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, thickness=2)
                id = employeelist[matchIndex]
                if counter == 0:
                    # Define the text and its position
                    text = "Loading"
                    text_position = (275, 400)

                    # Define the font parameters
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 1
                    font_color = (255, 255, 255)
                    font_thickness = 2

                    # Get the size of the text
                    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)

                    # Calculate the position for the bounding box
                    text_x, text_y = text_position
                    box_top_left = (text_x, text_y - text_size[1])
                    box_bottom_right = (text_x + text_size[0], text_y)

                    # Draw the bounding box rectangle
                    cv2.rectangle(imgBackground, box_top_left, box_bottom_right, (0, 0, 255), cv2.FILLED)

                    # Put the text on the image
                    cv2.putText(imgBackground, text, text_position, font, font_scale, font_color, font_thickness)

                    cv2.imshow("Face Attendance", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

        if counter != 0:

            if counter == 1:
                # Get the Data
                employeeInfo = db.reference(f'Employee/{id}').get()
                print(employeeInfo)
                # Get the Image from the storage
                blob = bucket.get_blob(f'images/{id}.jpg')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgEmployee = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                # Update data of attendance
                datetimeObject = datetime.strptime(employeeInfo['last_attendance_time'],
                                                   "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                print(secondsElapsed)
                if secondsElapsed > 30:
                    ref = db.reference(f'Employee/{id}')
                    employeeInfo['total_attendance'] += 1
                    ref.child('total_attendance').set(employeeInfo['total_attendance'])
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    # Write attendance to Excel sheet
                    write_to_excel(employeeInfo['name'])
                else:
                    modeType = 3
                    counter = 0
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

            if modeType != 3:

                if 10 < counter < 20:
                    modeType = 2

                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if counter <= 10:
                    cv2.putText(imgBackground, str(employeeInfo['total_attendance']), (861, 125),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(employeeInfo['major']), (1006, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(id), (1006, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(employeeInfo['standing']), (910, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(employeeInfo['year']), (1025, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(employeeInfo['starting_year']), (1125, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                    (w, h), _ = cv2.getTextSize(employeeInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(imgBackground, str(employeeInfo['name']), (808 + offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                    imgBackground[175:175 + 216, 909:909 + 216] = imgEmployee

                counter += 1

                if counter >= 20:
                    counter = 0
                    modeType = 0
                    employeeInfo = []
                    imgEmployee = []
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    else:
        modeType = 0
        counter = 0
    # cv2.imshow("Webcam", img)
    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)