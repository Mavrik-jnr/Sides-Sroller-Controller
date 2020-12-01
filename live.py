#Imports
import cv2
from pynput.keyboard import Controller
import numpy as np
import time



#keyboard controller object

keyboard = Controller()

#Function for input (note: This was configured for a game)
def Press(key):
    #The game i made it for had a special animation for this key input. So a delay was added.
    if key == 'b':
        keyboard.press(key)
        # time.sleep(0.1)
    keyboard.press(key)
def Press2 (key, key2):
    keyboard.press(key)
    keyboard.press(key2)
#Variables
x,y,k = 600,480,5

# Origin coordinate Function in which user selects, and moves tracked object about selected point

def Origin(event, x1,y1,flag, params):
    global x, y, k
    if event == cv2.EVENT_LBUTTONDOWN:
        x= x1
        y= y1
        k= 1 #Sets to 1 to close window 'user' immediately after click


#sends mouse clicked location to the Origin function
cv2.namedWindow('User')
cv2.setMouseCallback('User', Origin)
cap = cv2.VideoCapture(0)

#Live Videocam starts here

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    grey_old = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('User', frame)
    if (cv2.waitKey(1) == 27)  or (k ==1) :
        cv2.destroyAllWindows()
        # cap.release()
        break

#Centre is the reshaped x,y coordinates from the Origin function. (Reshaped for the optical flow function)
centre = np.array([x,y], dtype='float32').reshape(-1,1,2)
#made a copy so as to define distance between new tracked points given from Optical flow function and the set Origin
origin = centre.copy()


#Optical flow Section


#Made a Mask to be overlayed and show tracked object's movements
mask = np.zeros_like(frame)

#The loop to keep the tracking window open and also use the Optical flow Equation
while True:
    _, new_frame = cap.read()
    new_frame = cv2.flip(new_frame, 1)
    grey_new = cv2.cvtColor(new_frame,cv2.COLOR_BGR2GRAY)
    new_pos, status, err = cv2.calcOpticalFlowPyrLK(grey_old, grey_new, centre,None, maxLevel = 1, criteria= (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    #A Simple For loop to extract our calculated points and previous point
    for i , j in zip(centre, new_pos):
        x,y = i.ravel()
        a,b = j.ravel()
        #line trail
        cv2.line(mask, (a,b),(x,y), (0,0,255), 2)


    #Coordinate Points in origin extracted
    for i in origin:
        c,v = i.ravel()
        cv2.circle(mask,(c,v), 10, (0,255,0), -1 )


####  Distance evaluation and input mapping function   #### THIS WAS CONFIGURED FOR A SIDE SCROLLER GAME (PLAYDEAD'S INSIDE) ###

    X_dist = a - c
    Y_dist = b - v

    #For X direction away from origin (condition values are in pixels)



    if (X_dist < -30) & (X_dist > -50):
        keyboard.release('e')
        Press('a')

    elif X_dist <= -50:
        Press2('a', 'e')

    else :
        keyboard.release('a')

    if (X_dist > 30) & (X_dist < 50):
        keyboard.release('e')
        Press('d')

    elif X_dist >= 50:
        Press2('d', 'e')

    else:

        keyboard.release('d')


    #For Y direction away from origin (condition values are also in pixels)
    if (Y_dist < -5) & (Y_dist > -10):
        keyboard.release('e')
        Press('w')

    elif (Y_dist < -13) & (Y_dist > -35):
        keyboard.release('e')
        Press('b')


    elif Y_dist <= -40:
       Press2('w', 'e')

    else:
        keyboard.release('w')
        keyboard.release('b')

    if (Y_dist > 20) & (Y_dist < 40):
        keyboard.release('e')
        Press('s')

    elif Y_dist > 50:
        Press2('s','e')

    else:

        keyboard.release('s')


    #The Code to display tracking with overlay

    new_frame = cv2.addWeighted(mask, 0.2, new_frame, 0.8, 0)
    cv2.imshow('show', new_frame)
    grey_old = grey_new
    centre = new_pos.reshape(-1, 1, 2)

    if cv2.waitKey(1) == 27:
        break
cv2.destroyAllWindows()