import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from scipy.ndimage.filters import gaussian_filter
import matplotlib.cm as cm

def to_rgb2(im):
    # as 1, but we use broadcasting in one line
    im = np.asarray(im)
    w, h = im.shape
    ret = np.empty((w, h, 3), dtype=np.uint8)
    ret[:, :, :] = im[:, :, np.newaxis]
    return ret

def spotlight(im,heatmap,toplot=True):
    
    #if len(im.size)==2:
    #    im_new = to_rgb2(im)
    #    im = Image.fromarray(im_new, 'RGB')
    
    h=Image.fromarray(heatmap)
    h=h.resize(im.size)
    h=np.double(h)/255
    a=np.zeros(h.shape)
    
    n_levels=5
    a=np.zeros(h.shape)
    endpt=95-n_levels*5
    which_prctiles = range(100,endpt,-5)
    h_flat=h
    k=h_flat.flatten('F')


    for i in [80,85,90,95,100]:
        h50=np.percentile(h_flat,i)
        h50mat=np.copy(h)
        h50mat[h50mat<h50]=0
        h50mat[h50mat>0]=1
        a+=h50mat
    a_orig=a
    a=a/4
#     a=dilation(a,square(5))
    a = gaussian_filter(a, sigma=30)
#     a = remove_small_objects(a)
    a[a<0.2]=0.2


    singleim=np.single(im)/255

    b=np.array([a,a,a])
    b=b.transpose((1,2,0))
    r_channel=singleim[:,:,0]
    g_channel=singleim[:,:,1]
    b_channel=singleim[:,:,2]
    r_channel=np.multiply(a,r_channel)
    g_channel=np.multiply(a,g_channel)
    b_channel=np.multiply(a,b_channel)


    #z=np.asarray([r_channel,g_channel,b_channel])
    #z=z.transpose((1,2,0))
    rgb=np.dstack((r_channel,g_channel,b_channel))
    rgb[rgb>1]=1
    rgb_uint8 = (rgb * 255.999) .astype(np.uint8)
    z = Image.fromarray(rgb_uint8)
    
    if toplot:
        plt.figure(figsize=(20,20))
        plt.imshow(z,vmin=0,vmax=1)
        plt.axis('off')
        plt.show()
        #z=np.uint8(z*255)
        #zim = Image.fromarray(z)
    
    return z



def heatmap_overlay(im,heatmap,colmap='hot'):
    cm_array = cm.get_cmap(colmap)
    im_array = np.asarray(im)
    heatmap_norm = (heatmap-np.min(heatmap))/float(np.max(heatmap)-np.min(heatmap))
    heatmap_hot = cm_array(heatmap_norm)
    res_final = im_array.copy()
    #res_final[inds,...] = res2_hot[inds,0:3]*255.0*alpha + res3[inds,...]*(1-alpha)
    #res_final[...] = res2_hot[...,0:3]*255.0*alpha + res3[...]*(1-alpha)
    heatmap_rep = np.repeat(heatmap_norm[:, :, np.newaxis], 3, axis=2)
    res_final[...] = heatmap_hot[...,0:3]*255.0*heatmap_rep + im_array[...]*(1-heatmap_rep)
    return res_final


def heatmap_patches(im,heatmap,alpha=.6,colmap='hot'):
    cm_array = cm.get_cmap(colmap)
    im_array = np.asarray(im)
    heatmap_norm = (heatmap-np.min(heatmap))/float(np.max(heatmap)-np.min(heatmap))
    inds = heatmap_norm>(np.mean(heatmap_norm)+np.std(heatmap_norm))
    heatmap_hot = cm_array(heatmap_norm)
    res_final = im_array.copy()
    res_final[inds,...] = heatmap_hot[inds,0:3]*255.0*alpha + im_array[inds,...]*(1-alpha)
    return res_final
