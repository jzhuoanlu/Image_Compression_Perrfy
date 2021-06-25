from bs4 import *
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


def gen_directory():
    """ Generates an empty directory named "images." If one already exist, it 
    would override it.

    Returns
    -------
    dir_name : String
        return dir_name = "images" on success and None at failure (I'm thinking about changing this implemenation up)
    """

    dir_name = "images"
    try:
        os.mkdir(dir_name)
    except FileExistsError:
        # if the directory already exists, then delete it and recreate it
        try:
            shutil.rmtree(dir_name)
            os.mkdir(dir_name)
        except:
            return None
    return dir_name


def download_images(url, images, dir_name):
    """ Download images from their src url into a directory named dir_name 

    Parameters
    ----------
    images : ResultSet
        Set of <img> tags retrieved from the url
    dir_name : String
        name of directory where the images are saved

    Returns
    -------
    success : boolean
        return true on successfully downloading all the images and false 
        otherwise
    """

    count = 0 

    # if there are no images in the website, return success
    if images == None or len(images) == 0:
        return True
    
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
        
        # After getting Image Source URL
        # We will try to get the content of image
        try:

            # test to see if url is relative to base url.
            if not is_absolute(image_url):
                image_url = urljoin(url, image_url)
            r = requests.get(image_url).content
            
            try:
                # possibility of decode
                r = str(r, 'utf-8')
                
            except UnicodeDecodeError:
                
                # After checking above condition, Image Download start
                with open(f"{dir_name}/images{i+1}.jpg", "wb+") as f:
                    f.write(r)

                # counting number of image downloaded
                count += 1
        except:
            pass
        
    # if downloaded all the images, return True.
    if count == len(images):
        return True
    else:
        return False


def get_images(url):
    """ Returns a ResultSet containing all the <img> tags from the website specified by the given url.

    Parameters
    ----------
    url : str
        The url of the website being scrapped

    Returns
    -------
    images : ResultSet
        a list of the <img> tags from the html of the website
    """
    
    # requests.get sends a GET request to the specified url. Returns a 
    # response object
    r = requests.get(url)

    # beautiful soup grabs the text of the HTML file and uses html.parser to 
    # parse throug it
    soup = BeautifulSoup(r.text, 'html.parser')

    # parse through the HTML text and grab all the instances of "img"
    images = soup.findAll('img')

    return(images)
