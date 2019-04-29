from PIL import Image
import os
import sys

BASE = "../assets/task_data/"

dirs = ["all_images", "sentinel_CC", "natural", "tutorial_CC", "real_CC", "sentinel_images", "tutorial_sentinels", "real_images", "tutorial_images"]

def get_bad_ims(base, dirs): 
    n = 0
    bad = []
    dirs_to_check = [os.path.join(base, d) for d in dirs]
    for d in dirs_to_check: 
        for path, subdirs, files in os.walk(d):
            for name in files: 
                im_path = os.path.join(path, name)
                n += 1
                if not _is_valid_img(im_path): 
                    bad.append(name)
    print("Checked %d imgs" % n)
    return bad
                

def _is_valid_img(im_path): 
    try: 
        Image.open(im_path)
        return True
    except: 
        return False

if __name__ == "__main__": 
    #print(_is_valid_img("valid.jpg"))
    base = None
    if len(sys.argv) == 1: 
        print("Using % as base path" % BASE)
        base = BASE
    else: 
        base = sys.argv[1]
    print(base)
    print(get_bad_ims(base, dirs))
