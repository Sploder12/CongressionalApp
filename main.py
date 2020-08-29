# import the necessary packages
import numpy as np
import argparse
import cv2
import time as tim
import os
import constant
import Tello3

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--confidence", type=float, default=0.5, help="minimum probobility to filter weak detections")
ap.add_argument("-t", "--threshold", type=float, default=0.3, help="threshold when applying non-maxima suppression")
ap.add_argument("-o", "--output", type=str, default="", help="path to (optional) output video file")
ap.add_argument("-d", "--display", type=int, default=1, help="whether or not output frame should be displayed")
args = vars(ap.parse_args())

# gets the frame in a safe way. Program will temporarily hang if reciever is writing the image
def getImage(instance):
    frame = instance.Bframe
    return frame

# load the COCO class labels our YOLO model was trained on
labelsPath = os.path.sep.join(["yolo-coco", "coco.names"])
print("""1: person
2: bicycle
3: car
4: motorbike
5: aeroplane
6: bus
7: train
8: truck
9: boat
10: traffic light
11: fire hydrant
12: stop sign
13: parking meter
14: bench
15: bird
16: cat
17: dog
18: horse
19: sheep
20: cow
21: elephant
22: bear
23: zebra
24: giraffe
25: backpack
26: umbrella
27: handbag
28: tie
29: suitcase
30: frisbee
31: skis
32: snowboard
33: sports ball
34: kite
35: baseball bat
36: baseball glove
37: skateboard
38: surfboard
39: tennis racket
40: bottle
41: wine glass
42: cup
43: fork
44: knife
45: spoon
46: bowl
47: banana
48: apple
49: sandwich
50: orange
51: broccoli
52: carrot
53: hot dog
54: pizza
55: donut
56: cake
57: chair
58: sofa
59: pottedplant
60: bed
61: diningtable
62: toilet
63: tvmonitor
64: laptop
65: mouse
66: remote
67: keyboard
68: cell phone
69: microwave
70: oven
71: toaster
72: sink
73: refrigerator
74: book
75: clock
76: vase
77: scissors
78: teddy bear
79: hair drier
80: toothbrush
0: ALL
Select an option: 
""")
x = input()
x = int(x)
if(x == 0):
	LABELS = open(labelsPath).read().strip().split("\n")
else:
	LABELS = constant.objects.get(x)

# derive the paths to the YOLO weights and model configuration
weightsPath = os.path.sep.join(["yolo-coco", "yolov3.weights"])
configPath = os.path.sep.join(["yolo-coco", "yolov3.cfg"])

# load our YOLO object detector trained on COCO dataset (80 classes)
print("[INFO] loading YOLO from disk...")
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

# determine only the *output* layer names that we need from YOLO
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# initialize the video stream and pointer to output video file
print("[INFO] accessing video stream...")
#vs = cv2.VideoCapture(args["input"] if args["input"] else 0)
writer = None

# instance of Tello3
instance = Tello3.telloSDK()	

# loop over the frames from the video stream
def detect_people(frame, net, ln):
	global classIDs
	global confidences
	global x
	global y
	# grab the dimensions of the frame and  initialize the list of
	# results
	(H, W) = frame.shape[:2]
	results = []

	# construct a blob from the input frame and then perform a forward
	# pass of the YOLO object detector, giving us our bounding boxes
	# and associated probabilities
	blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
		swapRB=True, crop=False)
	net.setInput(blob)
	layerOutputs = net.forward(ln)

	# initialize our lists of detected bounding boxes, centroids, and
	# confidences, respectively
	boxes = []
	centroids = []
	confidences = []
	classIDs = []

	# loop over each of the layer outputs
	for output in layerOutputs:
		# loop over each of the detections
		for detection in output:
			# extract the class ID and confidence (i.e., probability)
			# of the current object detection
			scores = detection[5:]
			classID = np.argmax(scores)
			confidence = scores[classID]

			# filter detections by (1) ensuring that the object
			# detected was a person and (2) that the minimum
			# confidence is met
			if confidence > args["confidence"]:
				# scale the bounding box coordinates back relative to
				# the size of the image, keeping in mind that YOLO
				# actually returns the center (x, y)-coordinates of
				# the bounding box followed by the boxes' width and
				# height
				box = detection[0:4] * np.array([W, H, W, H])
				(centerX, centerY, width, height) = box.astype("int")

				# use the center (x, y)-coordinates to derive the top
				# and and left corner of the bounding box
				x = int(centerX - (width / 2))
				y = int(centerY - (height / 2))

				# update our list of bounding box coordinates,
				# centroids, and confidences
				boxes.append([x, y, int(width), int(height)])
				centroids.append((centerX, centerY))
				confidences.append(float(confidence))
				classIDs.append(classID)

	# apply non-maxima suppression to suppress weak, overlapping
	# bounding boxes
	idxs = cv2.dnn.NMSBoxes(boxes, confidences, args["confidence"], args["threshold"])

	# ensure at least one detection exists
	if len(idxs) > 0:
		# loop over the indexes we are keeping
		for i in idxs.flatten():
			# extract the bounding box coordinates
			(x, y) = (boxes[i][0], boxes[i][1])
			(w, h) = (boxes[i][2], boxes[i][3])

			# update our results list to consist of the person
			# prediction probability, bounding box coordinates,
			# and the centroid
			r = (confidences[i], (x, y, x + w, y + h), centroids[i])
			results.append(r)

	# return the list of results
	return results
while True:
	# Below is where the frame is entered
	# read the next frame from the file
	#(grabbed, frame) = vs.read()

	# if the frame was not grabbed, then we have reached the end
	# of the stream
	#if not grabbed:
		#break

	# resize the frame and then detect people (and only people) in it
	tim.sleep(0.05)
	frame = getImage(instance)
	print(frame, "NEW FRAME") #frames start repeating itself for some reason

	#Make sure you end it when done!

	results = detect_people(frame, net, ln)

	# loop over the results
	for (i, (prob, bbox, centroid)) in enumerate(results):
		# extract the bounding box and centroid coordinates, then
		# initialize the color of the annotation
		(startX, startY, endX, endY) = bbox
		(cX, cY) = centroid
		color = (0, 255, 0)

		# draw (1) a bounding box around the person and (2) the
		# centroid coordinates of the person,
		cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
		text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
		cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

	# check to see if the output frame should be displayed to our
	# screen
	if args["display"] > 0:
		# show the output frame
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break

	# if an output video file path has been supplied and the video
	# writer has not been initialized, do so now
	if args["output"] != "" and writer is None:
		# initialize our video writer
		fourcc = cv2.VideoWriter_fourcc(*"MJPG")
		writer = cv2.VideoWriter(args["output"], fourcc, 25,
			(frame.shape[1], frame.shape[0]), True)

	# if the video writer is not None, write the frame to the output
	# video file
	if writer is not None:
		writer.write(frame)
instance.end()

