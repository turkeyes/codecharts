import os
import glob
from PIL import Image
from collections import Counter
import matplotlib.pyplot as plt

# resize all images to these max dimensions (to be consistent across experiments with different image sizes)
MAX_H = 1340 #1920 1920 resized to 1000, max height can be 700 so 700x(1920/1000)
MAX_W = 1920 
to_resize = True

def get_max_dims(allfiles):

    widths = []
    heights = []
    for file in allfiles:
        im = Image.open(file)
        width, height = im.size
        widths.append(width)
        heights.append(height)

    #print("Image widths:",Counter(widths).keys())
    #print("Image heights:",Counter(heights).keys())

    maxwidth = max(list(Counter(widths).keys()))
    maxheight = max(list(Counter(heights).keys()))
    
    if to_resize:
        ratio = min(MAX_W/maxwidth, MAX_H/maxheight)
        maxwidth = int(maxwidth*ratio)
        maxheight = int(maxheight*ratio)
    
    return maxwidth,maxheight

def save_padded_images(real_image_dir,allfiles,toplot=False,maxwidth=None,maxheight=None):
    
    if maxwidth==None or maxheight==None:
        maxwidth,maxheight = get_max_dims(allfiles)
        
    print('Padding %d image files to dimensions: [%d,%d]...'%(len(allfiles),maxwidth,maxheight))

    for file in allfiles:
        #print(file)
        im = Image.open(file)
        
        if to_resize:
            #resize image to fixed dimensions
            width, height = im.size
            ratio = min(MAX_W/width, MAX_H/height)
            newwidth = int(width*ratio)
            newheight = int(height*ratio)
            im = im.resize((newwidth,newheight), Image.ANTIALIAS)
        
        width, height = im.size
        padded_im = Image.new('RGB',
                         (maxwidth, maxheight),  
                         (126, 126, 126)) 
        offset = ((maxwidth - width) // 2, (maxheight - height) // 2)
        padded_im.paste(im, offset)
        padded_im.save(os.path.join(real_image_dir,os.path.basename(file)))

        if toplot:
            plt.figure(figsize=(10,10))
            plt.imshow(padded_im)
            plt.axis('off');
            plt.show();
    
    print('Done!')
    return maxwidth,maxheight
            
        
if __name__ == "__main__":
    
    sourcedir = '../../importance_dataset/predimportance/analysis/CVs_all' # take images from here
    rootdir = './task_data'
    
    real_image_dir = os.path.join(rootdir,'real_images')
    if not os.path.exists(real_image_dir):
        print('Creating directory %s'%(real_image_dir))
        os.makedirs(real_image_dir)

    allfiles = glob.glob(os.path.join(sourcedir,'*.png'))

    save_padded_images(real_image_dir,allfiles,toplot=False)
    
    