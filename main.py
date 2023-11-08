import cv2
import numpy as np
import requests
import queue
import threading
import time
from vehicle_detector import VehicleDetector
import serial
import sys
import cvlib
from urllib.request import urlopen
import matplotlib.pyplot as plt

# IF NEEDED CHANGE THE LOCAL IP ADDRESS
URL = "http://192.168.244.163/capture"
URL2 = "http://192.168.244.69/capture"

#videoInput = cv2.VideoCapture(URL)
#videoInput2 = cv2.VideoCapture(URL2)

counter = 0
counter2 = 0
countTimeGreen1 = 0
countTimeRed1 = 0
countTimeGreen2 = 0
countTimeRed2 = 0

countCars = 0
sumTime = 0

portList = ['COM4', 'COM3', 'COM1', 'COM2']
counts = ['Green 1', 'Red 1', 'Green 2', 'Red 2']
listCountCars = []
listTime = []

class VideoCapture:
    def __init__(self, name):
        self.cap = cv2.VideoCapture(name)
        self.q = queue.Queue()
        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()

    def _reader(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()
                except queue.Empty:
                    pass
            self.q.put(frame)

    def read(self):
        return self.q.get()


def init():
    try:
        videoInput = urlopen(URL)
    except:
        print("Nao foi possivel conectar a camera 1")
        sys.exit()
    try:
        videoInput2 = urlopen(URL2)
    except:
        print("Nao foi possivel conectar a camera 2")
        sys.exit()
    try:
        vd = VehicleDetector()
    except:
        print("Nao foi possivel carregar o modulo de Deteccao.")
        sys.exit()
    try:
        ser = serial.Serial('COM5', 9600, timeout=1)
    except:
        print("Nao foi possível conectar ao Arduino.")
        sys.exit()
    return vd, ser

def captureImage():
    videoInput = urlopen(URL)
    videoInput2 = urlopen(URL2)
    arr = np.asarray(bytearray(videoInput.read()), dtype="uint8")
    arr2 = np.asarray(bytearray(videoInput2.read()), dtype="uint8")
    img = cv2.imdecode(arr, -1) # 'Load it as it is'
    img2 = cv2.imdecode(arr2, -1)
    return img, img2

#Funcao depreciada utilizada para inicialização da variável ser
"""def initializeSerial():
    try:
        ser = serial.Serial('COM4', 9600, timeout=1)
        return ser
    except:
        return "Porta Serial Indisponível no Arduino"""

def captureFrame(input):
    ret, frame = input.read()
    return frame

def findCars(countTimeGreen1, countTimeGreen2, countTimeRed1, countTimeRed2, countCars, sumTime):
    while True:
        #source = captureFrame(videoInput)
        #source2 = captureFrame(videoInput2)
        source, source2 = captureImage()
        vehicle_boxes = vd.detect_vehicles(source)
        vehicle_boxes2 = vd.detect_vehicles(source2)
        vehicle_count = len(vehicle_boxes)
        vehicle_count2 = len(vehicle_boxes2)
        print(f"Cruzamento 1: {vehicle_count}")
        print(f"Cruzamento 2: {vehicle_count2}")
        print("---")
        countCars = countCars + (len(vehicle_boxes)+len(vehicle_boxes2))
        listCountCars.append(countCars)
        #ser = initializeSerial()
        #ser.write(f'{vehicle_count}'.encode())
        #ser.write(f'{vehicle_count2}'.encode())
        if (vehicle_count>vehicle_count2):
            ser.write(b"G1R2")
            for i in range(0, 12):
                time.sleep(1)
                sumTime += 1
                countTimeGreen1 = countTimeGreen1 + 1
                countTimeRed2 = countTimeRed2 + 1
        elif (vehicle_count2>vehicle_count):
            ser.write(b"R1G2")
            for i in range(0, 12):
                time.sleep(1)
                sumTime += 1
                countTimeRed1 = countTimeRed1 + 1
                countTimeGreen2 = countTimeGreen2 + 1
        elif ((vehicle_count==0) or (vehicle_count2==0)):
            if ((vehicle_count==0) and (vehicle_count2==0)):
                ser.write(b"R1R2")
                for i in range(0, 12):
                    time.sleep(1)
                    sumTime += 1
                    countTimeRed1 = countTimeRed1 + 1
                    countTimeRed2 = countTimeRed2 + 1
            elif (vehicle_count==0):
                ser.write(b"R1G2")
                for i in range(0, 12):
                    time.sleep(1)
                    sumTime += 1
                    countTimeRed1 = countTimeRed1 + 1
                    countTimeGreen2 = countTimeGreen2 + 1
            elif (vehicle_count2==0):
                ser.write(b"G1R2")
                for i in range(0, 12):
                    time.sleep(1)
                    sumTime += 1
                    countTimeGreen1 = countTimeGreen1 + 1
                    countTimeRed2 = countTimeRed2 + 1
        listTime.append(sumTime)
        for box in vehicle_boxes:
            x, y, w, h = box
            cv2.rectangle(source, (x, y), (x+w, y+h), (25, 0, 180), 3)
            cv2.putText(source, f"{vehicle_count}", (20, 58), 0, 2, (108, 200, 0), 3)
        for box in vehicle_boxes2:
            x, y, w, h = box
            cv2.rectangle(source2, (x, y), (x+w, y+h), (25, 0, 180), 3)
            cv2.putText(source2, f"{vehicle_count2}", (20, 58), 0, 2, (108, 200, 0), 3)
        cv2.imshow('Source', source)
        cv2.moveWindow('Source', 0,0)
        cv2.imshow('Source 2', source2)
        if (cv2.waitKey(1) & 0xFF == ord('x')):
            return countTimeGreen1, countTimeGreen2, countTimeRed1, countTimeRed2, countCars

def plotting():
    fig, ax = plt.subplots()
    fig2, ax2 = plt.subplots()
    values = [countTimeGreen1, countTimeRed1, countTimeGreen2, countTimeRed2]
    ax.bar(counts, values)
    ax2.plot(listCountCars, listTime)
    print(listCountCars)
    print(listTime)
    plt.show()

vd, ser = init()
countTimeGreen1, countTimeGreen2, countTimeRed1, countTimeRed2, countCars = findCars(countTimeGreen1, countTimeGreen2, countTimeRed1, countTimeRed2, countCars, sumTime)
plotting()