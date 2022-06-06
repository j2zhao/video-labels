"""
Simple image attributes 
"""

from xml import dom
import cv2
import numpy as np
import os

def img_size(label, img_dir):
    name = label['name']
    dire = os.path.join(img_dir, name)
    img = cv2.imread(dire)
    return img.shape

def avg_bb_wrapper(funct):
    """
    wrapper function that finds the image attribute for bbox
    """
    def img_funct(label, img_dir):
        name = label['name']
        dire = os.path.join(img_dir, name)
        img = cv2.imread(dire)
        bbox = img[int(label['bbox']['x1']):int(label['bbox']['x2']), int(label['bbox']['y1']):int(label['bbox']['y2'])]
        value = funct(bbox)
        return value
    return img_funct

def img_color(img):
    color = np.mean(np.mean(img, axis=0), axis=0)
    return color

def img_dcolors(img, n_colors = 3):
    pixels = np.float32(img.reshape(-1, 3))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS
    _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)
    dominant = palette[np.argmax(counts)]
    return dominant

def img_lumin(img):
    if 0 in img.shape:
        return 0
    img = cv2.cvtColor(img, 40) # code: COLOR_BGR2HSV
    color = np.mean(np.mean(img, axis=0), axis=0)
    return color[2] # should be values in hsv

def img_edges(img, edges = False,edge_low = 100, edge_high = 200 ):
    # deeplens th1, th2 = edge_low=225, edge_high=250, but I used number in the example
    # to be more general (https://docs.opencv.org/3.4/dd/d1a/group__imgproc__feature.html#ga2a671611e104c093843d7b7fc46d24af)
    edges = cv2.Canny(img,edge_low,edge_high) 
    # average color with edges should be approximately how many edges there are relative to size
    if edges is None:
        return 0
    color = np.mean(edges)
    return color


