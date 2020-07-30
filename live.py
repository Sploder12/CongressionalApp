import cv2
import time

try:
    # Creates video object, 0 for external camera
    video=cv2.VideoCapture(0)

    # create frame object
    check, frame = video.read()
    print(check)
    print(frame)


    # shows the frame
    cv2.imshow("Capturing", frame)

    # add key to exit (milliseconds)
    cv2.waitKey(0)

    # shutdown the camera
    video.release()

    cv2.destroyAllWindows()
except:
    # Creates video object, 0 for external camera
    video=cv2.VideoCapture(1)

    # create frame object
    check, frame = video.read()
    print(check)
    print(frame)


    # shows the frame
    cv2.imshow("Capturing", frame)

    # add key to exit (milliseconds)
    cv2.waitKey(0)

    # shutdown the camera
    video.release()

    cv2.destroyAllWindows()