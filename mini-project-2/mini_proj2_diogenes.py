import numpy as np
import cv2 
import matplotlib.pyplot as plt 

cap = cv2.VideoCapture('CASSETA_PLANETA_ENTREVISTA_CABO_DACIOLO.mp4')
ret, frame = cap.read()
image = frame
#image = cv2.resize(frame, None, fx=0.4, fy=0.711, interpolation=cv2.INTER_AREA)
img = np.zeros((frame.shape[0],frame.shape[1],3), np.uint8)

drawing = False
ix = 0
iy = 0

flag1 = True
flag2 = False
flag_b = False

try:
    mascara = cv2.imread('mask_CASSETA_PLANETA_ENTREVISTA_CABO_DACIOLO.png')
    print(mascara.shape)
except:
    
# Adding Function Attached To Mouse Callback    
    def draw(event,x,y,flags,params):
        global ix,iy,drawing,flag_b
        # Left Mouse Button Down Pressed
        if(event==cv2.EVENT_LBUTTONDOWN):
            drawing = True
            ix = x
            iy = y

        if(event==cv2.EVENT_MOUSEMOVE):
            if(drawing==True):
                #For Drawing Line
                if flag_b == False:
                    cv2.line(img,pt1=(ix,iy),pt2=(x,y),color=(255,255,255),thickness=3)
                    ix = x
                    iy = y
                else:
                    cv2.line(img,pt1=(ix,iy),pt2=(x,y),color=(0,0,0),thickness=8)
                    ix = x
                    iy = y

        if(event==cv2.EVENT_LBUTTONUP):
            drawing = False

    # Making Window For The Image
    cv2.namedWindow("Window")

    # Adding Mouse CallBack Event
    cv2.setMouseCallback("Window",draw)

    # Starting The Loop So Image Can Be Shown
    while(True):

        dst = cv2.addWeighted(image,1,img,0.8,0)
        cv2.imshow('Window',dst)
        
        key = cv2.waitKey(25) & 0xFF

        if key == 27:
            cv2.imwrite('mask_CASSETA_PLANETA_ENTREVISTA_CABO_DACIOLO.png',img)      
            break        

        if key & 0xFF == ord('b'):
            flag_b = not flag_b

    cv2.destroyAllWindows()

while(True):
    
    if flag1 == True and flag2 == False:
        ret, frame = cap.read()
        #frame = cv2.resize(frame, None, fx=0.4, fy=0.711, interpolation=cv2.INTER_AREA)
        cv2.imshow('rst',frame)

    if flag2 == True and flag1 == False:
        ret, frame = cap.read()
        #frame = cv2.resize(frame, None, fx=0.4, fy=0.711, interpolation=cv2.INTER_AREA)
        frame_mask = cv2.imread('mask_CASSETA_PLANETA_ENTREVISTA_CABO_DACIOLO.png',0) 
        frame = cv2.inpaint(frame, frame_mask, 2, cv2.INPAINT_TELEA)
        cv2.imshow('rst',frame)

    
    key = cv2.waitKey(25) & 0xFF

    if key == 27:
        break        

    if key & 0xFF == ord('o'):
        flag1 = True
        flag2 = False
        
    if key & 0xFF == ord('i'):
        flag1 = False
        flag2 = True

cv2.destroyAllWindows()
