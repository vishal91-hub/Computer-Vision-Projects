import numpy
from ultralytics import YOLO
import cv2
model=YOLO('D:\Computer-Vision-Projects\YOLO-Weights\yolov8l.pt')
result=model("D:\Computer-Vision-Projects\images\image2.jpg",show= True)
cv2.waitKey(0)