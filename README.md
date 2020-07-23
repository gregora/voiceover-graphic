# Voiceover graphic

A simple tool to create nice graphics togeter with your .mp3 or .wav files.

## Dependencies
### Packages
* ffmpeg
### Python libraries:
* numpy
* cv2
* audio2numpy

## How do I use it?
Simple, run this by using `python3 main.py`.
A prompt should open, asking you to provide the path to all the necessary files.  
You will need:
* A sound file (.wav, .mp3, etc.)
* A logo file (.png, .jpg, etc.)
* A path to your output file

Example input:

![Example 1](https://imgur.com/coAPZLT.png)


After you have completed all the steps, the video should render, and you should get something like this:  
*The example is a still image, but obviously the output is a video*

![Example 2](https://i.imgur.com/zEQhU6m.png)


## Tips

* The logo image should always be bigger in the source file than in the final result, because if it upscales it will look awful.
* Default cricle color is the same as the first pixel in your image
* If you want to change circle color, you can do that in the code and change `custom_color` variable to `True`, and `color` variable to whatever you want
