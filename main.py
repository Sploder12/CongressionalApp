## to select which python script
#imports stuff
import os
#asks which image or video and gets the input to store in x
x = input("Select your option:\n1. Image\n2. Video\n")
x = int(x)
#selects image script
if x == 1:
    filename = input("Enter your filepath (images/): ")
#    outputpath = input("enter the output filename(output/): ")
    os.system("python yolo.py --image images/" + filename + " --yolo yolo-coco")
# " --output output/" + outputpath +
if x == 2:
    filename = input("Enter your filepath (videos/): ")
    outputpath = input("enter the output filename(output/): ")
    os.system("python yolo.py --image videos/" + filename + " --output output/" + outputpath + " --yolo yolo-coco")

