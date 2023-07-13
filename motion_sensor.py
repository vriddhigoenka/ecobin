import time
import cv2
from datetime import datetime
import imutils

#Create observer method to notify observer about changes in motion.

class MotionSensor:
    cap = None
    optimized = None
    initial = None
    detect = True
    motor = None
    
    def __init__(self, cap, optimized, motor):
        self.cap = cap
        self.optimized = optimized
        self.motor = motor
    
    def notify(self):
        self.motor.close_servo()
        self.optimized.classify()
        self.motor.open_servo()
        time.sleep(2)
        self.initial = None
        self.detect = True
        self.start()
    
    def changeDetect(self):
        self.detect = not self.detect

    def start(self):
        count = 2
        while self.detect:
            _, frame = self.cap.read()
            gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray_frame = cv2.GaussianBlur(gray_image, (21, 21), 0)
            if self.initial is None:
                time.sleep(2)
                self.initial = gray_frame
                continue
            differ_frame = cv2.absdiff(self.initial, gray_frame)
            thresh_frame = cv2.threshold(differ_frame, 30, 255, cv2.THRESH_BINARY)[1]
            thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)
            cont = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cont)
            self.initial = gray_frame
            if count < 0:

             for cur in cnts:
                print(cv2.contourArea(cur))
                if cv2.contourArea(cur) > 1000:
                    print("This was called")
                    self.detect = False
                    self.inital = None
                    return self.notify()
            else:
                count -= 1
