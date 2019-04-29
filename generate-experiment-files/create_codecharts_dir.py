import generate_codecharts
import os
import json 


def create_codecharts(real_CC_dir,ncodecharts,image_width,image_height):
    
    # new directory (will get populated in this file)
    if not os.path.exists(real_CC_dir):
        os.makedirs(real_CC_dir)
    # note: no buckets in this directory, all buckets will sample from a single source

    data = {}
    data_with_coords = {}
    for img_num in range(ncodecharts):
        if img_num%100==0:
            print('%d/%d'%(img_num,ncodecharts))
        filename = os.path.join(real_CC_dir,'real_CC_%d.jpg'%(img_num))
        valid_codes, coordinates = generate_codecharts.create_codechart(filename,image_width,image_height)
        data[filename] = {'valid_codes':valid_codes}
        data_with_coords[filename] = {'valid_codes':valid_codes, 'coordinates':coordinates}

    with open(os.path.join(real_CC_dir,'CC_codes.json'), 'w') as outfile: 
        json.dump(data, outfile)

    with open(os.path.join(real_CC_dir,'CC_codes_full.json'), 'w') as outfile: 
        json.dump(data_with_coords, outfile)
    
if __name__ == "__main__":
    
    rootdir = './task_data'

    # use these settings to figure out how many codecharts to make
    # so that each codechart will be sampled once
    num_subject_files = 200 #100    # default: 100 subject files/ bucket
    num_images_per_sf = 35 #20    # default: 20 images/ subject file
    ncodecharts = 2000 #num_subject_files*num_images_per_sf
    
    image_width = 1920 # in pixel
    image_height = 1080 # in pixel
    
    real_CC_dir = os.path.join(rootdir,'real_CC')
    
    create_codecharts(real_CC_dir,ncodecharts,image_width,image_height)
    