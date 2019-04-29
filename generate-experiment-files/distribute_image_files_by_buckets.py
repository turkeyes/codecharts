import os
import random
from shutil import copyfile
import glob

def distribute_images(from_dir,real_image_dir,num_buckets,start_bucket_at):
    # distribute images across buckets
    
    img_files = []
    for ext in ('*.jpeg', '*.png', '*.jpg'):
        img_files.extend(glob.glob(os.path.join(from_dir, ext)))

    random.shuffle(img_files) # shuffle all images randomly at start 
    images_per_bucket = int(len(img_files)/float(num_buckets))

    for b in range(num_buckets):
        bucket_dir = os.path.join(real_image_dir,'bucket%d'%(start_bucket_at+b))
        if not os.path.exists(bucket_dir):
            os.makedirs(bucket_dir)
        for i in range(b*images_per_bucket,b*images_per_bucket+images_per_bucket):
            destfile = os.path.basename(img_files[i])
            copyfile(img_files[i], os.path.join(bucket_dir,destfile))
        
if __name__ == "__main__":
    
    num_buckets = 1     # num buckets to split images into
    start_bucket_at = 0 # where to start the naming of the buckets (in case other buckets already exist)

    rootdir = './task_data'    

    real_image_dir = os.path.join(rootdir,'real_images')
    if not os.path.exists(real_image_dir):
        os.makedirs(real_image_dir)
        
    from_dir = os.path.join(rootdir,'all_images')

    distribute_images(from_dir,real_image_dir,num_buckets,start_bucket_at)