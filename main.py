import numpy as np
import argparse
import time as tim
import cv2
import os
import constant

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--input", required=True, help="1 for image 2 for drone")
ap.add_argument("-i", "--image", help="path to input")
ap.add_argument("-y", "--yolo", required=True, help="path to yolo DIR")
ap.add_argument("-c", "--confidence", type=float, default=0.5, help="minimum probobility to filter weak detections")
ap.add_argument("-t", "--threshold", type=float, default=0.3, help="threshold when applying non-maxima suppression")
args = vars(ap.parse_args())

# loads the drone stuff if needed
if args["input"] == "2":
	print("Now Loading: Tello3.py")
	import Tello3

# gets the frame in a safe way. Program will temporarily hang if reciever is writing the image
def getImage(instance):
    instance.mutexLock.acquire()
    frame = instance.Bframe
    instance.mutexLock.release()
    return frame # currently returns none, need to fix

# instance of Tello3
instance = Tello3.telloSDK()
speed = instance.sendMessage("speed?")
battery = instance.sendMessage("battery?")
time = instance.sendMessage("time?")
height = instance.sendMessage("height?")
temp = instance.sendMessage("temp?")
altitude = instance.sendMessage("altitude?")
barometer = instance.sendMessage("baro?")
acceleration = instance.sendMessage("acceleration?")
tof = instance.sendMessage("tof?") # idk what tof is
wifi = instance.sendMessage("wifi?")

# fix for multithreading issue
tim.sleep(0.08)

# gets the returned frame from the function
img = getImage(instance)

# load the COCO class labels our YOLO model was trained on
labelsPath = os.path.sep.join([args["yolo"], "coco.names"])
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
	print(LABELS)
else:
	LABELS = constant.objects.get(x)
	print(LABELS)
# initialize a list of colors to represent each possible class label
np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")

# derive the paths to the YOLO weights and model configuration
weightsPath = os.path.sep.join([args["yolo"], "yolov3.weights"])
configPath = os.path.sep.join([args["yolo"], "yolov3.cfg"])

# load our YOLO object detector trained on COCO dataset (80 classes)
print("[INFO] loading YOLO from disk...")
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

# load our input image and grab its spatial dimensions
if args["input"] == "1":
	image = cv2.imread(args["image"])
elif args["input"] == "2":
	image = img
(H, W) = image.shape[:2]

# determine only the *output* layer names that we need from YOLO
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# construct a blob from the input image and then perform a forward
# pass of the YOLO object detector, giving us our bounding boxes and
# associated probabilities
blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
net.setInput(blob)
start = tim.time()
layerOutputs = net.forward(ln)
end = tim.time()

# show timing information on YOLO
print("[INFO] YOLO took {:.6f} seconds".format(end - start))

# initialize our lists of detected bounding boxes, confidences, and
# class IDs, respectively
boxes = []
confidences = []
classIDs = []

# loop over each of the layer outputs
for output in layerOutputs:
	# loop over each of the detections
	for detection in output:
		# extract the class ID and confidence (i.e., probability) of
		# the current object detection
		scores = detection[5:]
		classID = np.argmax(scores)
		confidence = scores[classID]
		
		# filter out weak predictions by ensuring the detected
		# probability is greater than the minimum probability
		if confidence > args["confidence"]:
			# scale the bounding box coordinates back relative to the
			# size of the image, keeping in mind that YOLO actually
			# returns the center (x, y)-coordinates of the bounding
			# box followed by the boxes' width and height
			box = detection[0:4] * np.array([W, H, W, H])
			(centerX, centerY, width, height) = box.astype("int")
			
			# use the center (x, y)-coordinates to derive the top and
			# and left corner of the bounding box
			x = int(centerX - (width / 2))
			y = int(centerY - (height / 2))
			
			# update our list of bounding box coordinates, confidences,
			# and class IDs
			boxes.append([x, y, int(width), int(height)])
			confidences.append(float(confidence))
			classIDs.append(classID)

# apply non-maxima suppression to suppress weak, overlapping bounding
# boxes
idxs = cv2.dnn.NMSBoxes(boxes, confidences, args["confidence"], args["threshold"])

# ensure at least one detection exists
if len(idxs) > 0:
	# loop over the indexes we are keeping
	for i in idxs.flatten():
		# extract the bounding box coordinates
		(x, y) = (boxes[i][0], boxes[i][1])
		(w, h) = (boxes[i][2], boxes[i][3])

		# draw a bounding box rectangle and label on the image
		color = [int(c) for c in COLORS[classIDs[i]]]
		cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
		text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
		cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
# show the output image
cv2.imshow("Image", image)
cv2.waitKey(0)
#Make sure you end it when done!
instance.end()

