import cv2
from PIL import Image

def getFrames ():
    capture = cv2.VideoCapture("./videos/Fireworks.mp4")
    frameNr = 0

    while (frameNr < 50):
        success, frame = capture.read()
        if success:
            cv2.imwrite(f"./frames/{frameNr}.jpg", frame)
        else:
            break
        
        frameNr += 1

    capture.release()


def bwFrames ():
    i = 0
    while (i < 50):
        img = Image.open(f"./frames/{i}.jpg")
        img = img.convert("L")
        img.save(f"./frames/{i}.jpg")
        i += 1

getFrames()
bwFrames()

