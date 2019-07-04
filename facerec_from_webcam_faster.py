import face_recognition
import cv2
import numpy as np
from datetime import datetime
import time
import os

# Python code to remove duplicate elements 
def Remove(duplicate): 
	final_list = [] 
	for num in duplicate: 
		if num not in final_list: 
			final_list.append(num) 
	return final_list 

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)
global cnt 
global aux_
global old
global string_IN
global string_OUT
global flag_IN
global flag_OUT
cnt = 0
aux_ = 0
aux__ = 0
old = 0
string_IN = []
string_OUT = []
flag_IN = True
flag_OUT = False
unk = False
dict_ = {}
#file = open("out.txt","w")
#file = open("FACE_OUT.txt","w")

# Load a sample picture and learn how to recognize it.
image_1 = face_recognition.load_image_file("wallis.jpg")
face_encoding_image_1 = face_recognition.face_encodings(obama_image)[0]

# Load a second sample picture and learn how to recognize it.
#biden_image = face_recognition.load_image_file("obama.jpg")
#biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

#q = face_recognition.load_image_file("/home/default/Desktop/face_recognition_PDI/examples/DATA_SET_MV/"+"ID"+"-"+str(1)+".jpg")

india_image = face_recognition.load_image_file("India_Eisley.jpg")
india_face_encoding = face_recognition.face_encodings(india_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
	face_encoding_image_1,
#	biden_face_encoding,
	india_face_encoding
]

known_face_names = [
	"Diogenes",
#	"Obama",
	"India Eisley"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

ret, frame = video_capture.read()
frame = cv2.resize(frame, (0, 0), fx=1.4, fy=1.4)

image_unknown = np.zeros((frame.shape[0],frame.shape[1],3),np.uint8)

frame_IN = np.zeros((frame.shape[0],frame.shape[1],3),np.uint8)

while True:
    # Grab a single frame of video
	ret, frame = video_capture.read()
	ret, frame_aux = video_capture.read()

	frame_aux = cv2.resize(frame_aux, (0, 0), fx=1.4, fy=1.4)

	flag_detection = False
	time_detection_face_diogenes = 0
	#frame = cv2.resize(frame, (0, 0), fx=1.2, fy=1.2)
    # Resize frame of video to 1/4 size for faster face recognition processing
	small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
	rgb_small_frame = small_frame[:, :, ::-1]

	frame = cv2.resize(frame, (0, 0), fx=1.4, fy=1.4)
	
    # Only process every other frame of video to save time
	if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
		face_locations = face_recognition.face_locations(rgb_small_frame)
		face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

		face_names = []
		for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
			matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
			name = "Desconhecido"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
			face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
			best_match_index = np.argmin(face_distances)
			if matches[best_match_index]:
				name = known_face_names[best_match_index]

			face_names.append(name)
            #cv2.putText(frame, "face_detected", (0,70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 1)

	process_this_frame = not process_this_frame

    # Display the results
	for (top, right, bottom, left), name in zip(face_locations, face_names):

		flag_detection = True

        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
		top *= 5.6
		right *= 5.6
		bottom *= 5.6
		left *= 5.6
		top, right, bottom, left = int(top), int(right), int(bottom), int(left)
		
		if right < (int(frame.shape[1]/2)-10):
            # Draw a box around the face
			cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        
            # Draw a label with a name below the face
			cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        
		if left > (int(frame.shape[1]/2)+10):
            # Draw a box around the face
			cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 255), 2)
        
            # Draw a label with a name below the face
			cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 255), cv2.FILLED)
         
#        if right > 310 and left < 330:
#            flag_detection = False

		font = cv2.FONT_HERSHEY_DUPLEX

		cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

		if right < (int(frame.shape[1]/2)-10):

			#if name != "Desconhecido" and flag_IN == True:
			if flag_IN == True:
				if name != "Desconhecido":
					try:
						if reference == 0:
							reference = datetime.now()
							reference_ct = time.time()

						if reference != 0: 
							time_detection_face_diogenes = time.time() - reference_ct
		        	            
							if time.time() - reference_ct > 1:
								string_IN.append(name + " - " + str(reference) + "\n")
								flag_OUT = True
								flag_IN = False       
								print(time.time() - reference_ct)
					except:
						reference=0

			#if name == "Desconhecido" and flag_IN == True:
				if name == "Desconhecido":
					try:
						if reference == 0:
							reference = datetime.now()
							reference_ct = time.time()
							
		            
						if reference != 0: 
							time_detection_face_diogenes = time.time() - reference_ct
						
							if time.time() - reference_ct > 3:
								
								unk = True
								cnt += 1
								aux_top = max(0, top - 50)
								aux_bottom = min(bottom + 50,frame.shape[0])
								aux_left = max(0, left - 50)
								aux_right = min(right + 50,frame.shape[1])
			
								image_unknown = frame_aux[aux_top:aux_bottom,aux_left:aux_right]
								
								print("a")
								path1 = '/home/default/Desktop/face_recognition_PDI/examples/DATA_SET_UNKNOWN'
								cv2.imwrite(os.path.join(path1,"ID"+"-"+str(cnt)+".jpg"), image_unknown)
								#print("b")
								path2 = '/home/default/Desktop/face_recognition_PDI/examples/DATA_SET_MV'
								cv2.imwrite(os.path.join(path2,"ID" + "-" + str(cnt) + ".jpg"), image_unknown)			
								aux2 = "ID" + "-" + str(cnt) + "-_-"
								#print(cnt)			
								dict_[aux2] = face_recognition.load_image_file("/home/default/Desktop/face_recognition_PDI/examples/DATA_SET_MV/"+"ID"+"-"+str(cnt)+".jpg") 
								#print("zz")
								aux3 = "ID" + "-" + str(cnt) + "^_^"
								#print("z")
								try:			
									dict_[aux3] = face_recognition.face_encodings(dict_[aux2])[0]
									known_face_encodings.append(dict_[aux3])
									known_face_names.append("ID" + "-" + str(cnt))

								except:
									print("-" + str(cnt))			


								string_IN.append("ID" + "-" + str(cnt) + " - " + str(reference) + "\n")
								flag_OUT = True
								flag_IN = False
								#unk = False       
								print(string_IN)
					except:
						reference=0


		if left > (int(frame.shape[1]/2)+10):

			if name != "Desconhecido" and flag_OUT == True:
                
				try:
					if reference == 0:
						reference = datetime.now()
						reference_ct = time.time()
                    
					if reference != 0: 
						time_detection_face_diogenes = time.time() - reference_ct
                            
						if time.time() - reference_ct > 1:
							string_OUT.append(name + " - " + str(reference) + "\n")
							flag_OUT = False
							flag_IN = True                                  
				except:
					reference=0

		if right > (int(frame.shape[1]/2)-10) and left < (int(frame.shape[1]/2)+10):
			reference = 0


	if flag_detection == False:
		reference = 0
		aux = 0
    
	font = cv2.FONT_HERSHEY_SIMPLEX
    
	current_time = str(datetime.now())
    
	cv2.putText(frame, current_time, (0,20), font, 0.5, (255, 0, 0), 1)
	cv2.putText(frame, "Entry", (0,50), cv2.FONT_HERSHEY_TRIPLEX, 0.75, (255, 0, 0), 1)
	cv2.putText(frame, "Exit", (int(frame.shape[1]/2)+15,50), cv2.FONT_HERSHEY_TRIPLEX, 0.75, (255, 0, 0), 1)
	#print(frame.shape) 
	frame_IN[0:frame.shape[0],0:(int(frame.shape[1]/2)-10)] = frame[0:frame.shape[0],0:int(frame.shape[1]/2-10)]
	frame_IN[0:frame.shape[0],(int(frame.shape[1]/2)+10):frame.shape[1]] = frame[0:frame.shape[0],int(frame.shape[1]/2+10):frame.shape[1]]
    
    # Display the resulting image
	cv2.imshow('Video', frame_IN)

    # Hit 'q' on the keyboard to quit!
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# Release handle to the webcamfont = cv2.FONT_HERSHEY_SIMPLEX

string_IN = Remove(string_IN)
string_OUT = Remove(string_OUT)

outF = open("FACE_IN.txt", "w")
for line in string_IN:
  # write line to output file
	outF.write(line)
outF.close()

outF = open("FACE_OUT.txt", "w")
for line in string_OUT:
  # write line to output file
	outF.write(line)
outF.close()

"""num_lines = 0
with open("FACE_OUT.txt", 'r') as f:
	for line in f:
		num_lines += 1

file = open("FACE_NUMB.txt","w")
file.write("Diogenes - " + str(num_lines) + "\n")
file.close()"""

nomes = []

with open("FACE_OUT.txt", 'r') as f:
    for line in f:
        aux = line.split()
        nomes.append(aux[0])

cont = 0
cont_numb = []

for string in nomes:
    for i in range(len(nomes)):
        if string == nomes[i]:
            cont += 1
    cont_numb.append(string + " - " + str(cont) + "\n")
    cont = 0

cont_numb = Remove(cont_numb)

outF = open("FACE_NUMB.txt", "w")
for line in cont_numb:
  # write line to output file
	outF.write(line)
outF.close()


video_capture.release()
cv2.destroyAllWindows()
