import cv2
import numpy as np
import time
from vehicle_detector import VehicleDetector

videoInput = cv2.VideoCapture(0)
counter = 0

vd = VehicleDetector()

def captureFrame():
    ret, frame = videoInput.read()
    return frame

def findCars():
    while True:
        source = captureFrame()
        vehicle_boxes = vd.detect_vehicles(source)
        vehicle_count = len(vehicle_boxes)
        for box in vehicle_boxes:
            x, y, w, h = box
            cv2.rectangle(source, (x, y), (x+w, y+h), (25, 0, 180), 3)
            cv2.putText(source, f"{vehicle_count}", (20, 58), 0, 2, (108, 200, 0), 3)
        cv2.imshow('Source', source)
        if (cv2.waitKey(1) == 13):
            break
        time.sleep(1)

findCars()