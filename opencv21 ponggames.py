import cv2
import mediapipe as mp
print(cv2.__version__)

hands=mp.solutions.hands.Hands(False,2,1,0.5,0.5)
mpDrawing=mp.solutions.drawing_utils

def parseLamdmarks(frame):
    myHands=[]
    frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results=hands.process(frameRGB)

    if results.multi_hand_landmarks!=None:
        for handLms in results.multi_hand_landmarks:
            myhand=[]
            for landMark in handLms.landmark:
                myhand.append((int(landMark.x*width),int(landMark.y*height)))

            myHands.append(myhand)

    return myHands


width=720
height= 460 
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW) #camera object # DSHOW : DIRECT SHOW TO MAKE CAMERA LOAD FASTER

cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FPS,30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG')) # setting everything do that it runs smoothly on windows


paddlewidth=125
paddleheight=25
paddlecolor=(255,0,0)

ballcolor=(255,0,255)
ballradius=15
xpos=int(width/2)
ypos=int(height-10)
delx=10
dely=10

score=0
lives=3
font=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
 

ind=8

while True:
    ignore, frame = cam.read() # read a frame
    frame=cv2.resize(frame,(width,height))
    frame=cv2.flip(frame,1)

    cv2.circle(frame,(xpos,ypos),ballradius,ballcolor,-1)
    cv2.putText(frame,str(score),(25,int(paddleheight*3)),font,2,(0,255,0),5)
    cv2.putText(frame,str(lives),(width-125,int(paddleheight*3 )),font,2,(0,255,0),5)

    myHands=parseLamdmarks(frame)
    
    for hand in myHands:
        cv2.circle(frame,hand[8],5,(0,255,0),-1)
        cv2.rectangle(frame,(hand[8][0]-int(paddlewidth/2),0),(hand[8][0]+int(paddlewidth/2),paddleheight),paddlecolor,-1)

    topedgeball=ypos-ballradius
    bottomedgeball=ypos+ballradius
    leftedgeball=xpos-ballradius
    righedgeball=xpos+ballradius

    if leftedgeball<=0 or righedgeball>=width:
        delx*=-1
    if bottomedgeball>=height:
        dely*=-1

    if topedgeball<=paddleheight:
        if xpos>=int(hand[8][0]-(paddlewidth/2)) and xpos<int(hand[8][0]+int(paddlewidth/2)):
            dely*=-1
            score+=1

            if score%5==0 and score!=0:
                delx*=2
                dely*=2
        else:
            lives-=1
            xpos=int(width/2)
            ypos=int(height-10)



    xpos+=delx
    ypos+=dely

    

    if lives==0:
        cv2.putText(frame,"GAME OVER",(width//2-150,height//2),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,255),5)

        delx=0
        dely=0

    cv2.imshow('mycam1',frame) # show a frame
    cv2.moveWindow('mycam1',0,0)

    
    

    if cv2.waitKey(1) & 0xff == ord(' '):  # key to be pressed to exit 
        break

cam.release()

