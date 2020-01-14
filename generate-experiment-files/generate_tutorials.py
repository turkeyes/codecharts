import generate_codecharts
import generate_sentinels
import os
import string
import random
import json 
import matplotlib.pyplot as plt
import numpy as np
import base64 
import glob

def generate_tutorials(tutorial_image_dir,rootdir,image_width,image_height,border_padding,N,target_type,target_imdir,N_sent=0):
    
    if not os.path.exists(tutorial_image_dir):
        raise Exception('Please include a directory of tutorial images at: %s'%(tutorial_image_dir))

    tutorial_images = []
    for ext in ('*.jpeg', '*.png', '*.jpg'):
        tutorial_images.extend(glob.glob(os.path.join(tutorial_image_dir, ext)))
    print('A total of %d images will be sampled from for the tutorials.'%(len(tutorial_images)))
        
    tutorial_CC_dir = os.path.join(rootdir,'tutorial_CC')
    if not os.path.exists(tutorial_CC_dir):
        os.makedirs(tutorial_CC_dir)

    tutorial_sentinel_dir = os.path.join(rootdir,'tutorial_sentinels')
    if not os.path.exists(tutorial_sentinel_dir):
        os.makedirs(tutorial_sentinel_dir)

    # make the corresponding codecharts
    data = {}
    data_with_coords = {}
    for img_num in range(N):
        filename = tutorial_images[img_num]
        codechart_filename = os.path.join(tutorial_CC_dir,'tutorial_real_CC_%d.jpg'%(img_num))
        valid_codes, coordinates = generate_codecharts.create_codechart(codechart_filename,image_width,image_height)
        data[filename] = {'valid_codes':valid_codes,'flag':'tutorial_real','codechart_file':codechart_filename}
        data_with_coords[filename] = {'valid_codes':valid_codes, 'coordinates':coordinates,\
                                      'flag':'tutorial_real','codechart_file':codechart_filename}

    # now generate sentinel images (also N) with their corresponding codecharts  
    print('Populating %s with %d sentinel images'%(tutorial_sentinel_dir,N_sent))
    print('Populating %s with %d corresponding codecharts'%(tutorial_CC_dir,N_sent))
    for img_num in range(N_sent):
        codechart_filename = os.path.join(tutorial_CC_dir,'tutorial_sentinel_CC_%d.jpg'%(img_num))
        sentinel_filename = os.path.join(tutorial_sentinel_dir,'tutorial_sentinel_%d.jpg'%(img_num))
        D,D_full = generate_sentinels.make_sentinel(codechart_filename,sentinel_filename,\
                                                    image_width,image_height,border_padding,target_type, target_imdir)
        D['flag'] = 'tutorial_sentinel'
        D['codechart_file'] = codechart_filename
        D_full['flag'] = 'tutorial_sentinel'
        D_full['codechart_file'] = codechart_filename
        data[sentinel_filename] = D
        data_with_coords[sentinel_filename] = D_full

    with open(os.path.join(rootdir,'tutorial.json'), 'w') as outfile: 
        json.dump(data, outfile)
    print('Writing out %s'%(os.path.join(rootdir,'tutorial.json')))

    with open(os.path.join(rootdir,'tutorial_full.json'), 'w') as outfile: 
        json.dump(data_with_coords, outfile)
    print('Writing out %s'%(os.path.join(rootdir,'tutorial_full.json')))

    
if __name__ == "__main__":

    image_width = 1920 
    image_height = 1080 
    border_padding = 100 # don't put fixation cross in this region of the image
    rootdir = './task_data'
    target_type = "red_dot"
    target_imdir = ""

    tutorial_image_dir = os.path.join(rootdir,'tutorial_images')
    
    tutorial_images = glob.glob(os.path.join(tutorial_image_dir,'*.jpg'))
    N = len(tutorial_images)
    # assume that tutorial_images contains as many images (N) as desired for the tutorials    

    generate_tutorials(tutorial_image_dir,rootdir,image_width,image_height,border_padding,N,target_type,target_imdir)









