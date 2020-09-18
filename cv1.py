import cv2
import numpy as np
cap = cv2.VideoCapture('http://192.168.43.1:8080/videofeed')


def nothing(x):
    pass

cv2.namedWindow("Trackbars")
cv2.createTrackbar("L - H", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)
cv2.namedWindow("Trackbars_g")
cv2.createTrackbar("L g H", "Trackbars_g", 0, 255, nothing)
cv2.createTrackbar("L g S", "Trackbars_g", 0, 255, nothing)
cv2.createTrackbar("L g V", "Trackbars_g", 0, 255, nothing)
cv2.createTrackbar("U g H", "Trackbars_g", 255, 255, nothing)
cv2.createTrackbar("U g S", "Trackbars_g", 255, 255, nothing)
cv2.createTrackbar("U g V", "Trackbars_g", 255, 255, nothing)

if not cap.isOpened():
    print("Cannot open camera")
    exit()
# Set camera resolution
cap.set(3, 720)
cap.set(4, 360)

_, frame = cap.read()
rows, cols, _ = frame.shape

x_medium = int(cols / 2)
y_medium = int(rows / 2)
x_medium_b = int(cols / 2)
y_medium_b = int(rows / 2)
x_medium_g = int(cols / 2)
y_medium_g = int(rows / 2)
center = int(cols / 2)

while True:
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")
    low_blue = np.array([l_h, l_s, l_v])
    high_blue = np.array([u_h, u_s, u_v])

    # red color
    low_red = np.array([161, 155, 84])
    high_red = np.array([179, 255, 255])
    
    lgh = cv2.getTrackbarPos("L g H", "Trackbars_g")
    lgs = cv2.getTrackbarPos("L g S", "Trackbars_g")
    lgv = cv2.getTrackbarPos("L g V", "Trackbars_g")
    ugh = cv2.getTrackbarPos("U g H", "Trackbars_g")
    ugs = cv2.getTrackbarPos("U g S", "Trackbars_g")
    ugv = cv2.getTrackbarPos("U g V", "Trackbars_g")
    low_green = np.array([lgh, lgs, lgv])
    high_green = np.array([ugh, ugs, ugv])
    
    
    green_mask=cv2.inRange(hsv_frame, low_green, high_green)
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    blue_mask = cv2.inRange(hsv_frame, low_blue,high_blue)
     
    cont_green, _ =cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cont_red, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cont_blue, _ = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cont_red = sorted(cont_red, key=lambda x:cv2.contourArea(x) , reverse=True)
    cont_blue = sorted(cont_blue, key=lambda x:cv2.contourArea(x) , reverse=True)
    cont_green = sorted(cont_green, key=lambda x:cv2.contourArea(x) , reverse=True)
    
    for cnt in cont_red:
        (x, y, w, h) = cv2.boundingRect(cnt)
        
        x_medium = int((x + x + w) / 2)
        y_medium = int((y+y+h)/2)
        break
    for cnt in cont_blue:
        (x, y, w, h) = cv2.boundingRect(cnt)
        
        x_medium_b = int((x + x + w) / 2)
        y_medium_b = int((y+y+h)/2)
        break
    for cnt in cont_green:
        (x, y, w, h) = cv2.boundingRect(cnt)
        
        x_medium_g = int((x + x + w) / 2)
        y_medium_g = int((y+y+h)/2)
        break
   
    cv2.line(frame, (x_medium, 0), (x_medium, 480), (0, 0, 255), 2)
    cv2.line(frame, (0,y_medium),  (480,y_medium),(0,0,255),2)
    cv2.line(frame, (x_medium_b, 0), (x_medium_b, 480), (255, 0, 0), 2)
    cv2.line(frame, (0,y_medium_b),  (480,y_medium_b),(255,0,0),2)
    cv2.line(frame, (x_medium_g, 0), (x_medium_g, 480), (0, 255, 0), 2)
    cv2.line(frame, (0,y_medium_g),  (480,y_medium_g),(0,255,0),2)
    print (x_medium ,y_medium,sep=",")
    print (x_medium_b,y_medium_b,sep=",")
    print (x_medium_g,y_medium_g,sep=",", end="|||\n")
    cv2.imshow("greenm",green_mask)
    cv2.imshow("cont",blue_mask)
    cv2.imshow("frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break
    
    
cap.release()
cv2.destroyAllWindows()
