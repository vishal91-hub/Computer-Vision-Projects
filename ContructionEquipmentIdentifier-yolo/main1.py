from ultralytics import YOLO
import cv2
import math
import cvzone
cap=cv2.VideoCapture("D:\\Computer-Vision-Projects-yolo\\video\\ppe-1-1.mp4")
cap.set(3,640)
cap.set(4,480)

model=YOLO("D:\\Computer-Vision-Projects-yolo\\YOLO-Weights\\best.pt")
class_names = ['Excavator', 'Gloves', 'Hardhat', 'Ladder', 'Mask', 'NO-Hardhat', 'NO-Mask', 'NO-Safety Vest', 'Person', 'SUV', 'Safety Cone', 'Safety Vest', 'bus', 'dump truck', 'fire hydrant', 'machinery', 'mini-van', 'sedan', 'semi', 'trailer', 'truck and trailer', 'truck', 'van', 'vehicle', 'wheel loader']

while True:
    success, img=cap.read()
    results=model(img,stream=True)
    for r in results:
        boxes = r.boxes
        for box in boxes:
          #bounding box
          x1,y1,x2,y2=  box.xyxy[0]
          x1,y1,x2,y2=int(x1),int(y1),int(x2),int(y2)
          print(x1,y1,x2,y2)
          cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),3)
          
          #confidence level
          
          conf=math.ceil((box.conf[0]*100))/100
          print(conf)
          cvzone.putTextRect(img,f'{conf}',(max(0,x1),max(35,y1)))
          #class name
          
          cls=int(box.cls[0])
          cvzone.putTextRect(img,f'{conf}  {class_names[cls]}',(max(0,x1),max(35,y1)),scale=0.7,thickness=1)


    cv2.imshow("vi",img)
    cv2.waitKey(1)