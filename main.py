#audio stuff
from audio2numpy import open_audio

#video stuff
import cv2
import numpy as np
from cv2 import VideoWriter, VideoWriter_fourcc
import os
import math

#terminal color
import platform

if(platform.system() == "Linux"): #add colors to Linux terminal
    prefix = "\033[36m"
    suffix = "\033[39m"
else:
    prefix = ""
    suffix = ""

fp = input(prefix + "Name of your input file: " + suffix)
#fp = "inputs/sound.mp3"
print(prefix + "Opening audio file ..." + suffix)
signal, sampling_rate = open_audio(fp)

output_file = input(prefix + "Name of output file: " + suffix)
#output_file = "outputs/output.mp4"

upscale = int(input(prefix + "Upscale factor (2x recommended for HD, 4x for 4k): " + suffix))

logo_img = input(prefix + "Logo image: " + suffix)
print(prefix + "Opening logo file ..." + suffix)

print(prefix + "Sampling rate of audio file: " + suffix + str(sampling_rate))

list = []


c = 0

for i in signal:
    list.append((i[0] + i[1])/2)
    c+=1

width = 1920*upscale
height = 1080*upscale
FPS = 60
seconds = len(list) / sampling_rate
print(prefix + "Length of a video: " + suffix + str(int(seconds)) + " seconds")



img = cv2.imread(logo_img, -1)
img_w = len(img)
img_h = len(img[0])

img2 = np.zeros((img_w, img_h, 3))

for f in range(0, len(img) - 1):
    for c in range(0, len(img[f]) - 1):
        img2[f][c][0] = img[f][c][0]
        img2[f][c][1] = img[f][c][1]
        img2[f][c][2] = img[f][c][2]


logo_size = 240 * upscale #one side of a logo image in pixels

img2 = cv2.resize(img2, dsize=(logo_size, logo_size), interpolation=cv2.INTER_AREA)
img_h = len(img2)
img_w = len(img2[0])

img3 = img2[0:logo_size - 1, 0:logo_size - 1] #remove edges

custom_color = False
if(custom_color):
    color = [255, 255, 255] #default color
else:
    color = img[0][0].tolist() #take color from the first pixel in the image

srpfps = int(sampling_rate / FPS)
list2 = [];

for i in range(0, int(seconds * FPS)):
    sum = 0
    for j in range(0, srpfps):
        sum += abs(list[i*srpfps + j])

    if(i % 4 == 0):
        list2.append(sum / srpfps)

paint_h = int(height/2)

temporary_file = "/".join(output_file.split("/")[0:-1]) + "/temporary-" + output_file.split("/")[-1];
if(temporary_file[0] == "/"):
    temporary_file = temporary_file[1:]

fourcc = VideoWriter_fourcc(*'MP4V')
video = VideoWriter(temporary_file, fourcc, float(FPS), (width, height))

print(prefix + "Rendering video ..." + suffix)

for i in range(0, int(FPS * seconds)):
    frame = np.zeros((height, width, 3), dtype=np.uint8)

    try:

        if(i % 4 == 0):
            radius = list2[int(i / 4)] * 200
        elif(i % 4 == 1):
            radius = (list2[int((i - 1) / 4)] * 3/4 + list2[int((i + 3) / 4)] * 1/4) * 200
        elif(i % 4 == 2):
            radius = (list2[int((i - 2) / 4)] * 2/4 + list2[int((i + 2) / 4)] * 2/4) * 200
        elif(i % 4 == 3):
            radius = (list2[int((i - 3) / 4)] * 1/4 + list2[int((i + 1) / 4)] * 3/4) * 200

        radius = 200 + int(14 * math.sqrt(radius)) #nice, non linear function, that nicely represents quieter voices

    except:
        pass #sometimes the frames are not 100% nice


    cv2.circle(frame, (int(width/2), int(height/2)), radius*upscale, color, -1)
    frame = cv2.blur(frame,(3,3)) #this works as anti aliasing
    frame[int(height/2) - int(logo_size / 2):int(height/2) + int(logo_size / 2) - 1, int(width/2) - int(logo_size/2):int(width/2) + int(logo_size/2) - 1] = img3

    video.write(frame)
    if(i % 100 == 0):
        print(prefix + "Rendered frame " + str(i) + "/" + str(int(FPS * seconds)) + suffix)


video.release()
print(prefix + "Adding sound to the video ..." + suffix)
os.system("ffmpeg -i " + temporary_file + " -i " + fp + " -c:v copy -c:a aac " + output_file)
print(prefix + "Removing temporary file ...")
os.remove(temporary_file) #delete temporary file
print(prefix+"Finished with everything, output file - " + output_file + suffix)
