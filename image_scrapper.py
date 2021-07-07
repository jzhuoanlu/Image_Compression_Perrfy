from bs4 import *
from PIL import Image
import shutil
import requests
import os
from urllib.parse import urlparse, urljoin

def is_absolute(url):
    """ I want too look at this more, I'm not sure what .netloc is exactly
    Parameter
    ---------
    url : string
        url to test

    Returns
    -------
    : bool
        return whether or not the url is absolute
    """
    return bool(urlparse(url).netloc)


def gen_directory(path_to_dir):
    """ Generates an empty directory named "images." If one already exist, it 
    would override it.

    Returns
    -------
     : bool
        return True on success and False on failure (I'm thinking about changing this implemenation up)
    """

    try:
        os.mkdir(path_to_dir)
    except FileExistsError:
        # if the directory already exists, then delete it and recreate it
        try:
            shutil.rmtree(path_to_dir)
            os.mkdir(path_to_dir)
        except:
            return False
    return True


def compress_images(images_info, dir_name, quality):
    """ Download images from their src url into a directory named dir_name 
    Also adds the name of the compressed image to the image dictionary to be used to display
    Images that can't be compressed will contain a 'x' to show it wasn't compressed.

    Parameters
    ----------
    images_info : list[dict]
        list of dicts that contain info about the images
    dir_name : String
        name of directory where the images are saved
    quality : int
        percent quality of the image after compression

    Returns
    -------
    uncompressed : list[string]
        return a list of urls that were unable to be converted.
    """
    uncompressed = []
   
    for image_info in images_info:  
        # After getting Image Source URL
        # We will try to get the content of image
        image_info['compressed'] = None
        image_name = image_info["url"].rsplit('/', 1)[-1]
        try:
            path_to_image = dir_name + "/" + image_name
            image_info['compressed'] = image_name
            im = Image.open(requests.get(image_info["url"], stream=True).raw)
            im.save(path_to_image, optimize=True, quality=quality)
        except:
            image_info['compressed'] = 'x'
            uncompressed.append(image_info["url"])
            
    return uncompressed


def get_images(url):
    """ Returns a list of dictionaries that contain information about the 
    images. 
    Note: if src isn't found, then the image isn't returned in the list
    If src exists but either height or width doesn't exist, then add -1 for 
    height/width. (displaying with height/width of -1, just displays it as 
    intrensic value)

    Parameters
    ----------
    url : str
        The url of the website being scrapped

    Returns
    -------
    image_urls : list[dict{url: , width: , height:}]
        a list dicts that contain the url, width, and height of the images
    """

    # requests.get sends a GET request to the specified url. Returns a 
    # response object
    r = requests.get(url)

    # beautiful soup grabs the text of the HTML file and uses html.parser to 
    # parse throug it
    soup = BeautifulSoup(r.text, 'html.parser')

    # parse through the HTML text and grab all the instances of "img" return in a ResultSet
    images = soup.findAll('img')

    images_info = []
    # if there are no images in the website, return success
    if images == None or len(images) == 0:
        return images_info
    
    # loop through the images and retrieve the image source url
    for i, image in enumerate(images):
        # retreive the source url from these attributes in the following 
        # order. (I want to look into the HTMLOrForeignElement.dataset 
        # attributes more)
            # data-srcset
            # data-src
            # data-fallback-src
            # src
        image_info = {"url": None, "width": None, "height": None}
        
        try:
            image_url = image["data-srcset"]
        except:
            try:
                image_url = image["data-src"]
            except:
                try:
                    image_url = image["data-fallback-src"]
                except:
                    try:
                        image_url = image["src"]
                    # if no source url is found
                    except:
                        continue

        # test to see if url is relative to base url. If not, make it an absolute url
        if not is_absolute(image_url):
            image_url = urljoin(url, image_url)
        
        # 
        image_info["url"] = image_url

        # grab the height and the width of the images. if they don't specify height and width, then put -1
        try:
            image_info["width"] = image["width"]
        except:
            image_info["width"] = -1
        try:
            image_info["height"] = image["height"]
        except:
            image_info["height"] = -1

        images_info.append(image_info)
    return images_info