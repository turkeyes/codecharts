from PIL import Image, ImageDraw, ImageColor, ImageFont
import matplotlib.pyplot as plt
import numpy as np
import string
import random
import json 
import generate_codecharts as gc
import os

# FIXED parameters
text_color = ImageColor.getrgb("white")
font_type = "Arial.ttf"
px_pt_ratio = 20/29 # according to our image dimensions, 29 point = 20 px
valid_target_types=["red_dot", "fix_cross", "img"]

def make_sentinel(codechart_filename,sentinel_filename,image_width,image_height,border_padding,target_type="red_dot", target_im_dir=""):
    # border_padding used to guarantee that chosen sentinel location is not too close to border to be hard to spot
    
    font_size = int(image_height*0.0278)
    correct_codes = []
    
    if target_type not in valid_target_types: 
        raise RuntimeError("target_type must be one of %s" % valid_target_types.__str__())
    valid_codes, coordinates = gc.create_codechart(codechart_filename,image_width,image_height)
    # pick random code 
    r = list(range(0, len(valid_codes)))
    index = random.choice(r)
    triplet = valid_codes[index]
    triplet_coordinate = coordinates[triplet]
    # to make sure that the cross is visible
    while (triplet_coordinate[0] <= border_padding or triplet_coordinate[0] >= image_width-border_padding) \
    or (triplet_coordinate[1] <= border_padding or triplet_coordinate[1] >=image_height-border_padding): 
        index = random.choice(r)
        triplet = valid_codes[index]
        triplet_coordinate = coordinates[triplet]
    # check bg color
    if target_type == "fix_cross": 
        bg_color = 126
    else: 
        bg_color = 255
    # create and save cross sentinel image
    img = Image.new('RGB', (image_width, image_height), (bg_color, bg_color, bg_color))
    d = ImageDraw.Draw(img)
    try: 
        font = ImageFont.truetype(font_type, gc.pixel_to_point(font_size)) # takes in point value
    except OSError:
        print("WARNING: using different font bc could not find %d" % font_type)
        font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", gc.pixel_to_point(font_size))

    if target_type == "fix_cross":
        plot_coord = (triplet_coordinate[0]+font_size, triplet_coordinate[1]) # offset cross location to the center of the triplet
        d.text(plot_coord, '+', text_color, font)
    elif target_type == "red_dot":
        d.ellipse((triplet_coordinate[0], triplet_coordinate[1], triplet_coordinate[0]+font_size*2, triplet_coordinate[1]+font_size*2), fill = 'red', outline ='red')
    elif target_type == "img": 
        if not target_im_dir:
            raise RuntimeError("No im dir provided for sentinel targets")
        # Get a list of images in the target im dir
        images = os.listdir(target_im_dir)
        target = Image.open(os.path.join(target_im_dir, random.choice(images)))
        # resize the target 
        width = 200
        height = int(target.height*width/target.width)
        target = target.resize((width, height))
        plot_coord = (triplet_coordinate[0]-int(width/2), triplet_coordinate[1]-int(height/2))
        img.paste(target, plot_coord)
        
        # correct_codes lie within the sentinel width
        for ii in range(len(valid_codes)):
            dist = np.linalg.norm(np.array(coordinates[valid_codes[ii]])-np.array(triplet_coordinate))
            if dist <= width/2.0:
                correct_codes.append(valid_codes[ii]);
                
        pass
    else: 
        raise RuntimeError("target_type %s does not exist" % target_type)
    img.save(sentinel_filename)
    D = {'correct_code':triplet, 'coordinate':triplet_coordinate, 'correct_codes':correct_codes}
    D_full = {'correct_code':triplet, 'coordinate':triplet_coordinate, \
              'valid_codes':valid_codes, 'coordinates':coordinates, 'codechart_file':codechart_filename,\
              'correct_codes':correct_codes}
    return D,D_full

def generate_sentinels(sentinel_image_dir,sentinel_CC_dir,num_buckets,start_bucket_at,sentinel_images_per_bucket,\
                       image_width,image_height,border_padding,target_type,target_im_dir=""):
    
    # Set up directories
    if not os.path.exists(sentinel_image_dir):
        os.makedirs(sentinel_image_dir)
    if not os.path.exists(sentinel_CC_dir):
        os.makedirs(sentinel_CC_dir)
        
    # Start generating sentinels
    img_num_offset = (start_bucket_at-1)*sentinel_images_per_bucket # start at a new index id
    for b in range(num_buckets):

        image_bucket_dir = os.path.join(sentinel_image_dir,'bucket%d'%(start_bucket_at+b))
        if not os.path.exists(image_bucket_dir):
            os.makedirs(image_bucket_dir)

        CC_bucket_dir = os.path.join(sentinel_CC_dir,'bucket%d'%(start_bucket_at+b))
        if not os.path.exists(CC_bucket_dir):
            os.makedirs(CC_bucket_dir)

        data = {} # save to a json the filename, the coordinate of the + cross, and the triplet at that coordinate
        data_with_coords = {} # also save a list of other valid triplets and coordinates (for analysis)

        print('Populating %s with %d sentinel images'%(image_bucket_dir,sentinel_images_per_bucket))
        print('Populating %s with %d corresponding codecharts'%(CC_bucket_dir,sentinel_images_per_bucket))
        for i in range(sentinel_images_per_bucket):
            img_num = img_num_offset + b*sentinel_images_per_bucket + i + 1
            # generate random code chart
            codechart_filename = os.path.join(CC_bucket_dir,'sentinel_CC_%d.jpg'%(img_num))
            sentinel_filename = os.path.join(image_bucket_dir,'sentinel_image_%d.jpg'%(img_num))

            D,D_full = make_sentinel(codechart_filename,sentinel_filename,image_width,image_height,border_padding,target_type, target_im_dir)

            data[sentinel_filename] = D
            data_with_coords[sentinel_filename] = D_full

        with open(os.path.join(image_bucket_dir,'sentinel_codes.json'), 'w') as outfile: 
            json.dump(data, outfile)
        print('Writing out %s'%(os.path.join(image_bucket_dir,'sentinel_codes.json')))

        with open(os.path.join(image_bucket_dir,'sentinel_codes_full.json'), 'w') as outfile: 
            json.dump(data_with_coords, outfile)
        print('Writing out %s'%(os.path.join(image_bucket_dir,'sentinel_codes_full.json')))


if __name__ == "__main__":
    
    # Set these parameters
    sentinel_images_per_bucket = 500 
    num_buckets = 1 
    start_bucket_at = 0 # to avoid overwriting the existing buckets
    
    image_width = 1920 
    image_height = 1080 
    border_padding = 100 # don't put fixation cross in this region of the image
    rootdir = './task_data'

    target_type = "img" 
    target_im_dir = "sentinel_target_images"

    sentinel_image_dir = os.path.join(rootdir,'sentinel_images')
    sentinel_CC_dir = os.path.join(rootdir,'sentinel_CC')
    
    generate_sentinels(sentinel_image_dir,sentinel_CC_dir,num_buckets,start_bucket_at,sentinel_images_per_bucket,\
                       image_width,image_height,border_padding,target_type, target_im_dir)
    
    
