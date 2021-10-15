from __future__ import division
import cv2
import numpy as np
import math
import time
import paho.mqtt.client as mqtt


start=False

#connecting with wifi module
#def on_connect(client, userdata, flags, rc):
 #   print("Connected with result code " + str(rc))
  #  client.subscribe ("/leds/pi")
#reading message from wifi module
#def on_message(client ,userdata, msg):
 #   print(msg.topic+" "+str(msg.payload))
    
#def order(command):
 #   client.publish('/leds/esp8266',command)
    
#connecting
#client= mqtt.Client()
#client.on_contact = on_connect
#client.on_message=on_message
#client.connect('localhost', 1883,60)
#client.loop_start()
#Here is a problem,, just typing for hactober fest PR
    
def dis_ball_goal():
    dbg=math.sqrt(abs(pow((goal_x-ball_x),2)-pow((goal_y-ball_y),2)))
    return dbg
def imp():
    dbg=(dis_ball_goal())
    dgp=dbg+ext
    rx=int(((dgp*ball_x)-(ext*goal_x))/(dbg))
    ry=int(((dgp*ball_y)-(ext*goal_y))/(dbg))
    return rx, ry
def ang_car_imgp():
    if (car_front_x-car_back_x)==0:
        mc=math.inf
    else:
        mc=(car_front_y-car_back_y)/(car_front_x-car_back_x)
    if (img_x-car_front_x)==0:
        mbc=math.inf
    else:
        mbc=(img_y-car_front_y)/(img_x-car_front_x)
    ambc=int((math.degrees(math.atan(mc)))-(math.degrees(math.atan(mbc))))
    return ambc
def dis_bb():
    dimpc=math.sqrt(abs(pow((img_x-car_back_x),2)-pow((img_y-car_back_y),2)))
    return dimpc
def ang_car_ball():
    if (car_front_x-car_back_x)==0:
        mc=math.inf
    else:
        mc=(car_front_y-car_back_y)/(car_front_x-car_back_x)
    if (ball_x-car_front_x)==0:
        mbc=math.inf
    else:
        mbc=(ball_y-car_front_y)/(ball_x-car_front_x)
    ambc=int((math.degrees(math.atan(mc)))-(math.degrees(math.atan(mbc))))
    return ambc
def dis_car_imp():
    dimpc=math.sqrt(abs(pow((img_x-car_front_x),2)-pow((img_y-car_front_y),2)))
    return dimpc
def ang_car_goal():
    if (car_front_x-car_back_x)==0:
        mc=math.inf
    else:
        mc=(car_front_y-car_back_y)/(car_front_x-car_back_x)
    if (goal_x-ball_x)==0:
        mbc=math.inf
    else:
        mbc=(goal_y-ball_y)/(goal_x-ball_x)
    ambc=int((math.degrees(math.atan(mc)))-(math.degrees(math.atan(mbc))))
    return ambc
def dis_car_goal():
    dimpc=math.sqrt(abs(pow((goal_x-car_front_x),2)-pow((goal_y-car_front_y),2)))
    return dimpc 
def dis_cc():
    dimpc=math.sqrt(abs(pow((goal_x-car_back_x),2)-pow((goal_y-car_back_y),2)))
    return dimpc


print('script is running, press Ctrl+c to quit...') 

command='.'#initialising command variable

#start video capture
cap = cv2.VideoCapture(1)
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
cv2.createTrackbar("L B H", "ball", 29, 255, nothing)
cv2.createTrackbar("L B S", "ball", 166, 255, nothing)
cv2.createTrackbar("L B V", "ball", 105, 255, nothing)
cv2.createTrackbar("U B H", "ball", 41, 255, nothing)
cv2.createTrackbar("U B S", "ball", 255, 255, nothing)
cv2.createTrackbar("U B V", "ball", 198, 255, nothing)
cv2.namedWindow("car_front")
cv2.createTrackbar("L CF H", "car_front", 107, 255, nothing)
cv2.createTrackbar("L CF S", "car_front", 140, 255, nothing)
cv2.createTrackbar("L CF V", "car_front", 84, 255, nothing)
cv2.createTrackbar("U CF H", "car_front", 118, 255, nothing)
cv2.createTrackbar("U CF S", "car_front", 209, 255, nothing)
cv2.createTrackbar("U CF V", "car_front", 240, 255, nothing)
cv2.namedWindow("car_back")
cv2.createTrackbar("L CR H", "car_back", 63, 255, nothing)
cv2.createTrackbar("L CR S", "car_back", 118, 255, nothing)
cv2.createTrackbar("L CR V", "car_back", 87, 255, nothing)
cv2.createTrackbar("U CR H", "car_back", 90, 255, nothing)
cv2.createTrackbar("U CR S", "car_back", 192, 255, nothing)
cv2.createTrackbar("U CR V", "car_back", 213, 255, nothing)


ball_x = int(FRAME_WIDTH / 2)
ball_y = int(FRAME_HEIGHT / 2)
car_front_x = int(FRAME_WIDTH / 2)
car_front_y = int(FRAME_HEIGHT / 2)
car_back_x = int(FRAME_WIDTH / 2)
car_back_y = int(FRAME_HEIGHT / 2)
center = int(FRAME_WIDTH / 2)
goal_x = 0
goal_y = int(FRAME_HEIGHT/2)

ext=100
img_x=ball_x
img_y=ball_y

s1 = False
s2 = False
s3 = False
s4 = False

 

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
    uCFs = cv2.getTrackbarPos("U CF S",    "car_front")
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
    cv2.imshow("car_front",CF_mask)
    cv2.imshow("car_back",CR_mask)
    cv2.imshow("ball",ball_mask)
    
    img_x,img_y = imp()
    cv2.line(frame, (img_x, 0), (img_x, FRAME_HEIGHT), (25, 100, 5), 2)
    cv2.line(frame, (0,img_y),  (FRAME_WIDTH,img_y),(25,100,5),2)
    cv2.imshow("frame", frame)
    
    
    
    
    
    if start==True:
        print("*")
        if (not (((ang_car_imgp()>-5 and ang_car_imgp()<5) or (ang_car_imgp()<-175 and ang_car_imgp()>175))) or dis_car_goal()>dis_bb()) and s1==False:
            command = 'R'
            s2=True
            s3=True
            s4=True
            print(command)
        else:
            s1=True
            s2=False
            s3=True
            s4=True
        if dis_bb()>20 and s2==False:
            command ='F'
            s3=True
            s4=True
            print(command)
        else:
            s2=True
            s3=False
            s4=True
        if (not (((ang_car_ball()>-15 and ang_car_ball()<15) or (ang_car_ball()<-165 and ang_car_ball()>165))) or dis_car_goal()>dis_cc()) and s3==False:
            command = 'R'
            s4=True
            print(command)
        else:
            s3=True
            s4=True
    print(ang_car_imgp(), "ang")

   # rdoder(command)
    key = cv2.waitKey(50)
    if key == 32:
       start=True
       time.sleep(2) 
    if key == 27:
        break
   
cap.release()
cv2.destroyAllWindows()
