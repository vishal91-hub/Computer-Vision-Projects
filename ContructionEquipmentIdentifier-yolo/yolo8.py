# -*- coding: utf-8 -*-
"""yolo8.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NELZ3pS24LBYRknLbWxFZSOk8TqdNYEH
"""

!nvidia-smi

pip install ultralytics

from ultralytics import YOLO

!yolo task=detect mode=predict model=yolov8l.pt conf=0.25 source="https://ultralytics.com/images/bus.jpg"

#Custom data Training
!yolo task=detect mode=train model=yolov8l.pt data=../content/drive/MyDrive/dataset/Construction_Site_Safety/data.yaml epochs=50 imgsz=640