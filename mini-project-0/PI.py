import vrep
import cv2
import array
import numpy as np
import time
from PIL import Image as I

print('program started')
vrep.simxFinish(-1)
clientID=vrep.simxStart('127.0.0.1',19997,True,True,5000,5)
print ('Connected to remote API server')
r, colorCam = vrep.simxGetObjectHandle(clientID, "kinect_rgb", vrep.simx_opmode_oneshot_wait);
r, leftmotor = vrep.simxGetObjectHandle(clientID, "Pioneer_p3dx_leftMotor", vrep.simx_opmode_oneshot_wait);
r, rightmotor = vrep.simxGetObjectHandle(clientID, "Pioneer_p3dx_rightMotor", vrep.simx_opmode_oneshot_wait);

vrep.simxSetJointTargetVelocity(clientID, leftmotor, 0, vrep.simx_opmode_streaming);
vrep.simxSetJointTargetVelocity(clientID, rightmotor, 0, vrep.simx_opmode_streaming);

r, resolution, image = vrep.simxGetVisionSensorImage(clientID, colorCam, 1, vrep.simx_opmode_streaming);
time.sleep(0.5)

###
lm = 1
rm = -1
cx = 0
cnt = 0
###

while True:
	r, resolution, image = vrep.simxGetVisionSensorImage(clientID, colorCam, 1, vrep.simx_opmode_buffer);
	mat = np.asarray(image, dtype=np.uint8) 
	mat2 = mat.reshape(resolution[1], resolution[0], 1)
###
	vrep.simxSetJointTargetVelocity(clientID, leftmotor, lm, vrep.simx_opmode_streaming);
	vrep.simxSetJointTargetVelocity(clientID, rightmotor, rm, vrep.simx_opmode_streaming);
###	
	image = cv2.flip(mat2, 0)
###	
	img_limiar = cv2.threshold(image,100,255,cv2.THRESH_BINARY)
	img2 = img_limiar[1]
	cv2.imshow('robot camera', img2)
###

###		
	for i in range(640):
		if (img2[240,i]==0):
			cx = cx + i
			cnt = cnt + 1

	if cx > 0:
		dist = cx/cnt - 320
		cx = 0
		cnt = 0
		#print(dist,lm,rm)
		if dist < 0 and lm > rm:
			lm =  0.9 - dist/300
			rm =  2.1 
		if dist > 0 and rm > lm:
			rm =  0.9 - dist/300
			lm = 2.1 
###
	cv2.waitKey(1)
