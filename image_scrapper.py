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


def compress_images(image_urls, dir_name, quality):
    """ Download images from their src url into a directory named dir_name 

    Parameters
    ----------
    image_urls : list[string]
        image urls from the scrapped website
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

    for image_url in image_urls:  
        # After getting Image Source URL
        # We will try to get the content of image
        try:
            im = Image.open(requests.get(image_url, stream=True).raw)
            im.save(dir_name + "/" + image_url.rsplit('/', 1)[-1], optimize=True, quality=quality)
        except:
            uncompressed.append(image_url)
            
    return uncompressed


def get_image_urls(url):
    """ Returns a list of the absolute source urls for the images specified by the given url.

    Parameters
    ----------
    url : str
        The url of the website being scrapped

    Returns
    -------
    image_urls : list[string]
        a list of the absolute image urls on the website
    """

    image_urls = []
    
    # requests.get sends a GET request to the specified url. Returns a 
    # response object
    r = requests.get(url)

    # beautiful soup grabs the text of the HTML file and uses html.parser to 
    # parse throug it
    soup = BeautifulSoup(r.text, 'html.parser')

    # parse through the HTML text and grab all the instances of "img" return in a ResultSet
    images = soup.findAll('img')
    
    # if there are no images in the website, return success
    if images == None or len(images) == 0:
        return image_urls
    
    # loop through the images and retrieve the image source url
    for i, image in enumerate(images):
        # retreive the source url from these attributes in the following 
        # order. (I want to look into the HTMLOrForeignElement.dataset 
        # attributes more)
            # data-srcset
            # data-src
            # data-fallback-src
            # src
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

        image_urls.append(image_url)

    return(image_urls)