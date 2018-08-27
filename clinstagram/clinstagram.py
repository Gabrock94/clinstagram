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


__version__ = '0.0.0.1' #Version Control

def main():
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:v", ["help",
                                                         "version",
                                                         "login"])
    except getopt.GetoptError:
        show_help()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            show_help()
            exit()
        if opt in ("-v", "--version"):
            show_version()
            exit()
        if opt in ("--login"):
            config = ConfigParser()
            config.read('config.ini')
            username, password = login_GUI()
            
            exit()
            
    try:
        config = ConfigParser()
        config.read('config.ini')
        username = config.get('credentials', 'username')
        password = config.get('credentials', 'password')
    except:
        print("Credentials not found. \n Please login first!")
        username, password = login_GUI()
        
    api = InstagramAPI(username, password)
    if(api.login()):   
        api.timelineFeed()  # get self user feed
        with open('data.json', 'w') as outfile:
            json.dump(api.LastJson, outfile)
            
        print("Login succes! Welcome back "+ username)
        parseFeed(api)
        
    else:
        print("Can't login!")
        
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
    #gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    gscale1 = '@%#*+=-:. '
    image = Image.open('img.jpg').convert('L')
    W, H = image.size[0], image.size[1]
    cols = 60
    w = W/cols
    h = w/0.5
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
  
            #gsval = gscale1[int((avg*69)/255)] 
            gsval = gscale1[int((avg*9)/255)] 
            aimg[j] += gsval 
    return("\n".join(aimg))
    
def parseFeed(api):
    with open('data.json','r') as data_file:
        feed = json.load(data_file)
    #return(feed)
    
    for picture in feed['items']:
        if('user' in picture.keys() and 'image_versions2' in picture.keys()):
            image_url = False
            image = picture['image_versions2']['candidates'][0]
            image_url = image['url']
                   
            if(image_url != False):
                response = requests.get(image_url, stream=True)
                with open('img.jpg', 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                del response
                print("\033[H\033[J")
                print("@"+picture['user']["username"]+" - "+picture['user']['full_name']+"\n")
                print(asciify())
                print(str(picture["like_count"]) + " ❤ - "+str(picture["comment_count"]) + " comments")
                if(picture['has_liked']):
                    print(" - You like this picture")
                print("\n")
                print(picture['caption']['text']+"+\n")
                while(True):
                    userInput = input(": (n = next, q = quit, l=like): ")
                    if(userInput == "n"):
                        break
                    if(userInput == "q"):
                        exit()
                    if(userInput == "l"):
                        print("Like added!")
                        api.like(picture['id'])
                    else:
                        print("Invalid Command")
                
    return(feed)
        
        

###############################################################################
#                                                                             #
#   This sections handles help and other oneliner options (version)           #
#                                                                             #
###############################################################################

def show_help():
    """ This functions shows the help menu """ 
    print (
        '\n  clInstagram is a unoffficial command line interface for Instagram.'
        'For more information visit https://www.github.com/gabrock94'
        '\n\n'
        '  usage:\n'
        '    --help, -h\t\tshows help\n'
        '    --version, -v\tshows version\n'
        '    --login \t\tcall the login function\n')
    
def show_version():
    print(__version__)

def login_GUI():
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    config = ConfigParser()
    config.read('config.ini')
    if(config.has_section('credentials') == False):
        config.add_section('credentials')
    config.set('credentials', 'username', username)
    config.set('credentials', 'password', password)
    with open('config.ini', 'w') as f:
        config.write(f)
    return([username, password])
    
if __name__ == "__main__":
    
    feed = parseFeed()
