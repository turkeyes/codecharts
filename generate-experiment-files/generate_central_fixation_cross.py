from PIL import Image, ImageDraw, ImageColor, ImageFont
import matplotlib.pyplot as plt
import numpy as np
import json 
import os

# FIXED parameters
text_color = ImageColor.getrgb("white")
font_type = "Arial.ttf"
px_pt_ratio = 20/29 # according to our image dimensions, 29 point = 20 px

def pixel_to_point(num): 
	return int(num*(1/px_pt_ratio))

def save_fixation_cross(rootdir,image_width,image_height):
    
    font_size = int(image_height*0.0278)
    print('using font size: %d'%(font_size))
    
    # Generate and save fixation cross image
    img = Image.new('RGB', (image_width, image_height), (126, 126, 126))
    d = ImageDraw.Draw(img)
    try: 
        font = ImageFont.truetype(font_type, pixel_to_point(font_size)) # takes in point value
    except OSError: 
        print("WARNING: using a different font because oculd not find %s on your computer" % font_type)
        font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", pixel_to_point(font_size))
    d.text((image_width/2.0 - font_size, image_height/2.0 - font_size), '+', text_color, font)
    filename = 'fixation-cross.jpg'
    img.save(os.path.join(rootdir,filename))

if __name__ == "__main__":
    
    rootdir = './task_data'
    image_width = 1920 # in pixel
    image_height = 1080 # in pixel
    
    
