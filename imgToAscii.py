import sys
from PIL import Image

def setBlackAndWhite (img):
    img = img.convert("L")
    return img

def getBrightnessFromChunk (width, offx, offy, img):
    px = img.load()
    i = offx
    tot = 0
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

# makes brightness non-inverted
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

def chunkToAscii (width, offx, offy, img):
    return brightnessToChar(getBrightnessFromChunk(width, offx, offy, img))

def asciiIfyImage (imgpath, precision):
    precision = int(precision)
    img = Image.open(imgpath)
    bwImage = setBlackAndWhite(img)
    finalOutput = ""
    j = 0
    while (j < (bwImage.size)[1]):
        i = 0
        while (i < (bwImage.size)[0]):
            finalOutput += chunkToAscii(precision, i, j, bwImage) + " "
            i += precision
        j += precision
        finalOutput += "\n"
    print(finalOutput)
    
asciiIfyImage(sys.argv[1], sys.argv[2])
