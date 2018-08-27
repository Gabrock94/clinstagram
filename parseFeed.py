#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 19:24:31 2018

@author: giulio
"""

import sys
import json
import getopt
import getpass            
import shutil
import requests
from InstagramAPI import InstagramAPI
from configparser import ConfigParser 
import sys
from PIL import Image
import numpy as np

def getAverageL(image): 
  
    """ 
    Given PIL Image, return average value of grayscale value 
    """
    # get image as numpy array 
    im = np.array(image) 
  
    # get shape 
    w,h = im.shape 
  
    # get average 
    return np.average(im.reshape(w*h)) 

def asciify():
    gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    image = Image.open('img.jpg').convert('L')
    W, H = image.size[0], image.size[1]
    cols = 50
    w = W/cols
    h = w/1
    rows = int(H/h)
    aimg = [] 
    for j in range(rows): 
        y1 = int(j*h) 
        y2 = int((j+1)*h) 
        if j == rows-1: 
            y2 = H 
        aimg.append("") 
        for i in range(cols): 
            x1 = int(i*w) 
            x2 = int((i+1)*w) 
            if i == cols-1: 
                x2 = W 
            img = image.crop((x1, y1, x2, y2)) 
            avg = int(getAverageL(img)) 
  
            gsval = gscale1[int((avg*69)/255)] 
            aimg[j] += gsval 
    return("\n".join(aimg))
    
def parseFeed():
    with open('data.json','r') as data_file:
        feed = json.load(data_file)
    #return(feed)
    
    for picture in feed['items']:
        if('user' in picture.keys() and 'image_versions2' in picture.keys()):
            print(picture['user']["username"])
            image_url = False
            image = picture['image_versions2']['candidates'][0]
            image_url = image['url']
                   
            if(image_url != False):
                response = requests.get(image_url, stream=True)
                with open('img.jpg', 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                del response
                
                print(asciify())
                

    return(feed)
    
feed = parseFeed()
        