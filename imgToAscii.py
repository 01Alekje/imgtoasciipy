import sys
import os
import cv2
from PIL import Image


def setBlackAndWhite (img):
    img = img.convert("L")
    return img


def getBrightnessFromChunk (width, offx, offy, img):
    px = img.load()
    tot = 0

    i = offx
    while (i < width + offx and i < img.size[0]):
        j = offy
        while (j < width + offy and j < img.size[1]):
            tot += px[i, j]
            j += 1
        i += 1
    tot = tot/(width*width)
    return tot


# makes brightness inverted
def brightnessToCharInverted (bns):
    match bns:
        case bns if bns > 225:
            return '.'
        case bns if bns > 200:
            return ':'
        case bns if bns > 175:
            return '+'
        case bns if bns > 150:
            return ')'
        case bns if bns > 125:
            return 'f'
        case bns if bns > 100:
            return 'z'
        case bns if bns > 75:
            return 'O'
        case bns if bns > 50:
            return 'a'
        case bns if bns > 25:
            return '%'
        case _:
            return '$'


# clearer b/w distinction
def brightnessToCharContrast (bns):
    match bns:
        case bns if bns > 200:
            return '$'
        case bns if bns > 125:
            return ')'
        case bns if bns > 75:
            return ':'
        case _:
            return ' '


# more brightness-variations, to use with high (low) precision and big monitors
def brightnessToCharPristine (bns):
    match bns:
        case bns if bns > 250:
            return '$'
        case bns if bns > 250:
            return 'B'
        case bns if bns > 235:
            return '8'
        case bns if bns > 220:
            return '#'
        case bns if bns > 205:
            return 'h'
        case bns if bns > 190:
            return 'd'
        case bns if bns > 175:
            return 'w'
        case bns if bns > 160:
            return 'L'
        case bns if bns > 135:
            return 'Z'
        case bns if bns > 120:
            return 'x'
        case bns if bns > 105:
            return '/'
        case bns if bns > 90:
            return '?'
        case bns if bns > 75:
            return '-'
        case bns if bns > 60:
            return '>'
        case bns if bns > 45:
            return 'I'
        case bns if bns > 30:
            return '"'
        case bns if bns > 15:
            return '.'
        case _:
            return ' '


# standard
def brightnessToChar (bns):
    match bns:
        case bns if bns > 225:
            return '$'
        case bns if bns > 200:
            return '%'
        case bns if bns > 175:
            return 'a'
        case bns if bns > 150:
            return 'o'
        case bns if bns > 125:
            return 'z'
        case bns if bns > 100:
            return 'f'
        case bns if bns > 80:
            return ')'
        case bns if bns > 60:
            return '+'
        case bns if bns > 35:
            return ':'
        case bns if bns > 25:
            return '.'
        case _:
            return ' '


def chunkToAscii (width, offx, offy, img, rMode):
    if rMode == "default":
        return brightnessToChar(getBrightnessFromChunk(width, offx, offy, img))
    elif rMode == "pristine":
        return brightnessToCharPristine(getBrightnessFromChunk(width, offx, offy, img))
    elif rMode == "contrast":
        return brightnessToCharContrast(getBrightnessFromChunk(width, offx, offy, img))
    elif rMode == "inverted":
        return brightnessToCharInverted(getBrightnessFromChunk(width, offx, offy, img))
    else:
        print("\n\tIncorrect argument " + "'" + rMode + "'. For help, simply dont enter any arguments. \n")
        exit(1)
        

def asciiIfyImage (imgpath, precision, writetofile, rMode):
    precision = int(precision)
    img = Image.open(imgpath)
    bwImage = setBlackAndWhite(img)
    finalOutput = ""

    j = 0
    while (j < (bwImage.size)[1]):
        i = 0
        while (i < (bwImage.size)[0]):
            finalOutput += chunkToAscii(precision, i, j, bwImage, rMode) + " "
            i += precision
        j += precision
        finalOutput += "\n"
    if writetofile == True:
        writeToFile(finalOutput)
    else:
        os.system('clear')
        print(finalOutput)


def writeToFile (finalOutput):
    open("./output/asciiArt.txt", 'w').close()
    f = open("./output/asciiArt.txt", "w")
    f.write(finalOutput)
    f.close()


def treatInput (argvls):
    video = False
    if len(argvls) <= 3:
        print("\n\t Example usage: python3 imgtoasciipy.py *'<path>/<to>/<image.xyz>', *'<precision>', *'<write to file>' '<render type>'\n")
        print("\t *precision: \n\t\t -An integer as string. Defines pixels/char. Lower is more precise.")
        print("\t *write to file: \n\t\t -'y' writes to file ./output/asciiArt.txt\n\t\t -'n' writes to this terminal window")
        print("\t render type: \n\t\t -Chooses render type. Options = [contrast, inverted, pristine, default={enter nothing}] \n")
    if len(argvls) >= 4:
        if argvls[3].lower() == 'y':
            wtf = True
        elif argvls[3].lower() == 'v':
            wtf = False
            prepVideo(argvls[1], int(argvls[2]))
        else:
            wtf = False
        if len(argvls) > 4:
            asciiIfyImage(argvls[1], int(argvls[2]), wtf, argvls[4].lower())
        else:
            asciiIfyImage(argvls[1], int(argvls[2]), wtf, "default")

# Exclusively video stuff

def getFrames (vidPath, frames):
    capture = cv2.VideoCapture(vidPath)

    frameNr = 0
    while (frameNr < frames):
        success, frame = capture.read()
        if success:
            cv2.imwrite(f"./frames/{frameNr}.jpg", frame)
        else:
            break
        
        frameNr += 1

    capture.release()


def bwFrames (frames):
    i = 0
    while (i < frames):
        img = Image.open(f"./frames/{i}.jpg")
        img = img.convert("L")
        img.save(f"./frames/{i}.jpg")
        i += 1


def prepVideo (vidPath, precision):
    frames = 2700
    getFrames(vidPath, frames)
    bwFrames(frames)
    i = 0
    while (i < frames):
        asciiIfyImage(f"./frames/{i}.jpg", precision, False, "default")
        print("\n\n")
        # Bigger i means faster video
        i += 3


# The function that starts it all
treatInput(sys.argv)