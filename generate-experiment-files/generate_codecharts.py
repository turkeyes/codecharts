from PIL import Image, ImageDraw, ImageColor, ImageFont
import matplotlib.pyplot as plt
import numpy as np
import string
import random
import json 
import os
import math

# DEFINE PARAMATERS 
forbidden_letters = set(["I", "O"]) # letters to not use in code charts because can be confused with digits
px_pt_ratio = 20/29 # according to our image dimensions, 29 point = 20 px
text_color = ImageColor.getrgb("gray")
font_type = "Arial.ttf"
tojitter = True # add jitter from a regular grid
ebuf = 5 # buffer number of pixels to leave from the edges of the image so codecharts are not tangent to image edges

def point_to_pixel(num): 
    return int(num*px_pt_ratio)

def pixel_to_point(num): 
    return int(num*(1/px_pt_ratio))

def generate_rand_letter(): 
    letter = random.choice(string.ascii_uppercase)
    while letter in forbidden_letters: 
        letter = random.choice(string.ascii_uppercase)
    return letter

def generate_rand_triplet(): 
    code = ""
    code += generate_rand_letter()
    # the following code prevents the two digits from being identical or equal to 0
    for i in range(2): 
        if i == 0:
            forbidden_num = 0
        else:
            forbidden_num = int(code[i])
        r = list(range(1, forbidden_num)) + list(range(forbidden_num+1, 10))
        code += str(random.choice(r))
    return code

def create_codechart(filename,image_width,image_height): 

    font_size = int(image_height*0.0185)
    
    # all these parameters depend on font size
    max_triplet_width = font_size*3 # in pixel - max triplet width; used 'W88' as widest triplet code (width~60, height=20) 
    max_triplet_height = font_size # the tallest a triplet can be
    d_v = 4*max_triplet_height # vertical distance to maintain b/w triplets in the grid
    d_h = 2*max_triplet_width # horizontal distance to maintain b/w triplets (from start of one triplet to start of another)
    
    # make sure that not too much empty space is left over by spacing out triplets
    N_h = int(math.floor((image_width-max_triplet_width-2*ebuf) / float(d_h))) # number of triplets that will be tiled horizontally
    d_h = int(math.floor((image_width-max_triplet_width-2*ebuf) / float(N_h))) # recompute the horizontal dist between triplets to eliminate extra space
    N_v = int(math.floor((image_height-max_triplet_height-2*ebuf) / float(d_v)))
    d_v = int(math.floor((image_height-max_triplet_height-2*ebuf) / float(N_v)))
    # -------------
    
    post_jitter_buffer = 6 # small buffer to cover edge case of triplets immediately adjacent to one another (for legibility)
    j_v = int(0.25*(d_v) - post_jitter_buffer/2) # max vertical jitter for one side of a triplet
    j_h = int(0.25*(d_h) - post_jitter_buffer) # max horizontal jitter for on side of a triplet  

    # set up image canvas and font size/style 
    img = Image.new('RGB', (image_width, image_height))
    d = ImageDraw.Draw(img)
    try: 
        font = ImageFont.truetype(font_type, pixel_to_point(font_size)) # takes in point value
    except OSError:
        print("WARNING: using a different font bc could not find %s on your computer" % font_type)
        font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", pixel_to_point(font_size))

    valid_codes = set()
    coordinates = {}
    
    for x in range(ebuf, image_width-max_triplet_width-ebuf, d_h): # regularly sample the image horizontally
        for y in range(ebuf, image_height-max_triplet_height-ebuf, d_v): # regularly sample the image vertically
            triplet_code = generate_rand_triplet()
            
            # check for if triplet has already been used in image since all codes should be unique
            while triplet_code in valid_codes: 
                triplet_code = generate_rand_triplet() 
            valid_codes.add(triplet_code)

            if tojitter:
                # implement jitter to x and y coordinates (note: can turn either of them off)
                min_x = max(ebuf,x-j_h)
                max_x = min(x+j_h+1,image_width-max_triplet_width-ebuf)
                min_y = max(ebuf,y-j_v)
                max_y = min(y+j_v+1,image_height-max_triplet_height-ebuf-2) # a little bit of extra buffer in vertical dimension
                x_range = list(range(min_x, max_x))
                y_range = list(range(min_y, max_y))
                j_x = random.choice(x_range)
                j_y = random.choice(y_range)
            else:
                j_x = x
                j_y = y

            # writes triplet to image 
            d.text((j_x, j_y), triplet_code, text_color, font)
            coordinates[triplet_code] = (j_x, j_y)
            
    img.save(filename)
    return (list(valid_codes), coordinates)


if __name__ == "__main__":
    # create some code charts to test this code
    rootdir = './task_data'
    num_codecharts = 3 # generate this many codecharts
    
    #image_width = 1920 # in pixel
    #image_height = 1080 # in pixel
    
    image_height = 1340 #1344
    image_width = int(1036*image_height/float(1344))
    
    # set up directories
    if not os.path.exists(rootdir):
        os.makedirs(rootdir)
    test_dir = os.path.join(rootdir,'TEST')
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    
    data = {}
    for i in range(num_codecharts): 
        filename = os.path.join(test_dir,'CC_%d.jpg'%(i))
        valid_codes, coordinates = create_codechart(filename,image_width,image_height)
        data[filename] = (valid_codes, coordinates)

    with open(os.path.join(test_dir,'data.json'), 'w') as outfile: 
        json.dump(data, outfile)

