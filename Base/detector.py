import cv2
import numpy as np
import time

# Video input
#videoInput = cv2.VideoCapture(0)
videoInput = cv2.VideoCapture('sources/video.mp4')
#550 / 80
COUNTLINE_POSITION = 550
MIN_WIDTH_REACT = 70
MIN_HEIGHT_REACT = 70
OFFSET = 6 #Allow error between pixels
counter = 0

# Initializing the substractor
algorithm = cv2.bgsegm.createBackgroundSubtractorMOG()

def center_handle(x, y ,w, h):
    x1 = int(w/2)
    y1 = int(h/2)
    cx = x+x1
    cy = y+y1
    return cx, cy

detect = []

# Loop while for the running program
while True:
    ret, frame1 = videoInput.read()
    grayScale = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gaussianBlur = cv2.GaussianBlur(grayScale, (3, 3), 5)
    # Applying the algorithm to the frames
    imageSubstractor = algorithm.apply(gaussianBlur)
    dilateImage = cv2.dilate(imageSubstractor, np.ones((5,5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilatedImage = cv2.morphologyEx(dilateImage, cv2.MORPH_CLOSE, kernel)
    dilatedImage = cv2.morphologyEx(dilateImage, cv2.MORPH_CLOSE, kernel)
    counterShape, h = cv2.findContours(dilatedImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.line(frame1,(25, COUNTLINE_POSITION), (1200, COUNTLINE_POSITION), (255, 127, 0), 3)

    for (i, c) in enumerate(counterShape):
        (x, y, w, h) = cv2.boundingRect(c)
        validate_counter = (w>=MIN_WIDTH_REACT) and (h>=MIN_HEIGHT_REACT)
        if not validate_counter:
            continue
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 0, 255), 2)
        cv2.putText(frame1, f"VEHICLE {str(counter)}", (x, y-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 244, 0), 2)

        center = center_handle(x, y, w, h)
        detect.append(center)
        cv2.circle(frame1, center, 4, (0, 0, 255), -1)
        print(counter)

        for (x, y) in detect:
            if (y<(COUNTLINE_POSITION + OFFSET) and (y>(COUNTLINE_POSITION-OFFSET))):
                #counter+=1 
                pass
            cv2.line(frame1, (25, COUNTLINE_POSITION), (1200, COUNTLINE_POSITION), (0, 127, 255), 3)
            detect.remove((x, y))
            #print(f"Counter: {str(counter)}")
    
    cv2.putText(frame1, f"VEHICLE COUNTER: {str(counter)}", (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)

    cv2.imshow('Detecter', dilatedImage)

    cv2.imshow('Original Video', frame1)

    if cv2.waitKey(1) == 13:
        break
    time.sleep(1)

cv2.destroyAllWindows()
videoInput.release()