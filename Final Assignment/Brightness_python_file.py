#download the three libraries first then run the code else use python nootbook.

import cv2
import mediapipe as mp
import time
import wmi

bc = wmi.WMI(namespace='wmi')

mH=mp.solutions.hands
mD= mp.solutions.drawing_utils
hnd=mH.Hands()
camw=640
camh=480
cap = cv2.VideoCapture(0)
cap.set(3,camw) 
cap.set(4,camh)

c1x=0
c1y=0
c2x=0
c2y=0
mx=0
my=0
length=120
brightness=70
while True:
    
    success,img = cap.read()
    if not success:
        break
    
    imgrgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    r= hnd.process(imgrgb)
    
    if r.multi_hand_landmarks:


        for hlm in r.multi_hand_landmarks:
            lmList=[]
            for id,lm in enumerate(hlm.landmark):
                h,w,c=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                lmList.append([id,cx,cy])   
            c2x=lmList[8][1]
            c2y=lmList[8][2]
            cv2.circle(img,(c2x,c2y),10,(255,0,255),cv2.FILLED)
            c1x=lmList[4][1]
            c1y=lmList[4][2]
            cv2.circle(img,(c1x,c1y),10,(255,0,255),cv2.FILLED)
            length=pow(abs(c1x-c2x),2)+pow(abs(c1y-c2y),2)
            length=int(pow(length,0.5))
            mx=int((c1x+c2x)/2)
            my=int((c1y+c2y)/2)
            cv2.line(img,(c1x,c1y),(c2x,c2y),(255,0,0),2)
            if length<21:
                 cv2.circle(img,(mx,my),10,(0,255,0),cv2.FILLED)
                
            mD.draw_landmarks(img,hlm,mH.HAND_CONNECTIONS)
            
    if length<20:
        brightness=0
        
    elif length>180:
        brightness=100
    else:
     brightness = int((length-20)*100/160)
    bc.WmiMonitorBrightnessMethods()[0].WmiSetBrightness(brightness, 0) 
    perbr=brightness/100
    cv2.rectangle(img,(590,100),(555,400),(0,255*perbr,255*(1-perbr)),3)
    cv2.rectangle(img,(590,400-3*brightness),(555,400),(0,255*perbr,255*(1-perbr)),cv2.FILLED)
    cv2.putText(img,f'{brightness}%',(545,95),cv2.FONT_HERSHEY_PLAIN,2,(0,255*perbr,255*(1-perbr)),3)

    cv2.imshow("Image", img)
    if(cv2.waitKey(1) == ord('q')):
     break
 
cv2.destroyAllWindows()
cap.release()
