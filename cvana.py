#from __future__ import division
import cv2
import numpy as np
#import time

#import paho.mqtt.client as mqtt


# start=False
#connecting with wifi module
#def on_connect(client, userdata, flags, rc):
 #   print("Connected with result code " + str(rc))
  #  client.subscribe ("/leds/pi")
#reading message from wifi module
#def on_message(client ,userdata, msg):
   # print(msg.topic+" "+str(msg.payload))
   # start=True
#connecting
#client= mqtt.Client()
#client.on_contact = on_connect
#client.on_message=on_message
#client.connect('localhost', 1883,60)
#client.loop_start()

print('script is running, press Ctrl+c to quit...') 

command='.'#initialising command variable
#start video capture
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
#Set frame dimension
FRAME_WIDTH = 720
FRAME_HEIGHT = 360
cap.set(cv2.CAP_PROP_FRAME_WIDTH,FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,FRAME_HEIGHT)


def nothing(x):
    pass

#trackbars
cv2.namedWindow("ball")
cv2.createTrackbar("L B H", "ball", 0, 255, nothing)
cv2.createTrackbar("L B S", "ball", 0, 255, nothing)
cv2.createTrackbar("L B V", "ball", 0, 255, nothing)
cv2.createTrackbar("U B H", "ball", 255, 255, nothing)
cv2.createTrackbar("U B S", "ball", 255, 255, nothing)
cv2.createTrackbar("U B V", "ball", 255, 255, nothing)
cv2.namedWindow("car_front")
cv2.createTrackbar("L CF H", "car_front", 0, 255, nothing)
cv2.createTrackbar("L CF S", "car_front", 0, 255, nothing)
cv2.createTrackbar("L CF V", "car_front", 0, 255, nothing)
cv2.createTrackbar("U CF H", "car_front", 255, 255, nothing)
cv2.createTrackbar("U CF S", "car_front", 255, 255, nothing)
cv2.createTrackbar("U CF V", "car_front", 255, 255, nothing)
cv2.namedWindow("car_back")
cv2.createTrackbar("L CR H", "car_back", 0, 255, nothing)
cv2.createTrackbar("L CR S", "car_back", 0, 255, nothing)
cv2.createTrackbar("L CR V", "car_back", 0, 255, nothing)
cv2.createTrackbar("U CR H", "car_back", 255, 255, nothing)
cv2.createTrackbar("U CR S", "car_back", 255, 255, nothing)
cv2.createTrackbar("U CR V", "car_back", 255, 255, nothing)



ball_x = int(FRAME_WIDTH / 2)
ball_y = int(FRAME_HEIGHT / 2)
car_front_x = int(FRAME_WIDTH / 2)
car_front_y = int(FRAME_HEIGHT / 2)
car_back_x = int(FRAME_WIDTH / 2)
car_back_y = int(FRAME_HEIGHT / 2)
center = int(FRAME_WIDTH / 2)
goal_x = 0
goal_y = int(FRAME_HEIGHT/2)

while True:
    #taking frames
    _, frame = cap.read()

    cv2.imshow("frame", frame)
    #CONVERTING TO HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    #BALL COLOR VALUES
    lBh = cv2.getTrackbarPos("L B H", "ball")
    lBs = cv2.getTrackbarPos("L B S", "ball")
    lBv = cv2.getTrackbarPos("L B V", "ball")
    uBh = cv2.getTrackbarPos("U B H", "ball")
    uBs = cv2.getTrackbarPos("U B S", "ball")
    uBv = cv2.getTrackbarPos("U B V", "ball")
    low_ball = np.array([lBh, lBs, lBv])
    high_ball = np.array([uBh, uBs, uBv])

    # CAR FRONT COLOR VALUES
    lCFh = cv2.getTrackbarPos("L CF H", "car_front")
    lCFs = cv2.getTrackbarPos("L CF S", "car_front")
    lCFv = cv2.getTrackbarPos("L CF V", "car_front")
    uCFh = cv2.getTrackbarPos("U CF H", "car_front")
    uCFs = cv2.getTrackbarPos("U CF S", "car_front")
    uCFv = cv2.getTrackbarPos("U CF V", "car_front")
    low_CF = np.array([lCFh,lCFs, lCFv])
    high_CF = np.array([uCFh,uCFs, uCFv])
    
    # CAR BACK COLOR VALUE
    lgh = cv2.getTrackbarPos("L CR H", "car_back")
    lgs = cv2.getTrackbarPos("L CR S", "car_back")
    lgv = cv2.getTrackbarPos("L CR V", "car_back")
    ugh = cv2.getTrackbarPos("U CR H", "car_back")
    ugs = cv2.getTrackbarPos("U CR S", "car_back")
    ugv = cv2.getTrackbarPos("U CR V", "car_back")
    low_CR = np.array([lgh, lgs, lgv])
    high_CR = np.array([ugh, ugs, ugv])
    
    #creating color mask
    CR_mask=cv2.inRange(hsv_frame, low_CR, high_CR)
    CF_mask = cv2.inRange(hsv_frame, low_CF, high_CF)
    ball_mask = cv2.inRange(hsv_frame, low_ball,high_ball)

    cont_CR, _ =cv2.findContours(CR_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cont_CF, _ = cv2.findContours(CF_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cont_ball, _ = cv2.findContours(ball_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    cont_CF = sorted(cont_CF, key=lambda x:cv2.contourArea(x) , reverse=True)
    cont_ball = sorted(cont_ball, key=lambda x:cv2.contourArea(x) , reverse=True)
    cont_CR = sorted(cont_CR, key=lambda x:cv2.contourArea(x) , reverse=True)
    
    #taking pixel coordinates of different object
    for cnt in cont_CF:
        (x, y, w, h) = cv2.boundingRect(cnt)

        car_front_x = int((x + x + w) / 2)
        car_front_y = int((y+y+h)/2)
        break
    for cnt in cont_ball:
        (x, y, w, h) = cv2.boundingRect(cnt)

        ball_x = int((x + x + w) / 2)
        ball_y = int((y+y+h)/2)
        break
    for cnt in cont_CR:
        (x, y, w, h) = cv2.boundingRect(cnt)

        car_back_x = int((x + x + w) / 2)
        car_back_y = int((y+y+h)/2)
        break
   # DRAWING LINE OVER OBJECTS
    cv2.line(frame, (ball_x, 0), (ball_x, FRAME_HEIGHT), (40, 240, 235), 2)
    cv2.line(frame, (0,ball_y),  (FRAME_WIDTH,ball_y),(40,240,235),2)
    cv2.line(frame, (car_front_x, 0), (car_front_x,FRAME_HEIGHT), (255, 0, 0), 2)
    cv2.line(frame, (0,car_front_y),  (FRAME_WIDTH,car_front_y),(255,0,0),2)
    cv2.line(frame, (car_back_x, 0), (car_back_x, FRAME_HEIGHT), (0, 255, 0), 2)
    cv2.line(frame, (0,car_back_y),  (FRAME_WIDTH,car_back_y),(0,255,0),2)
    print (ball_x ,ball_y)
    cv2.imshow("car_front",CF_mask)
    cv2.imshow("car_back",CR_mask)
    cv2.imshow("ball",ball_mask)
    cv2.imshow("frame", frame)
 #   client.publish('/leds/esp8266',command)
 #   time.sleep(1000)

    key = cv2.waitKey(5)
    if key == 27:
        break
    
    
cap.release()
cv2.destroyAllWindows()



 

    

