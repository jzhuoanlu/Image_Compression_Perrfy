from PIL import Image
import os
import shutil
from urllib.parse import urlparse


# ****** incomplete ******

def gen_directory():
    """ Generates an empty directory named "images." If one already exist, it 
    would override it.

    Returns
    -------
    dir_name : String
        return dir_name = "compressed_images" on success and None at failure (I'm thinking about changing this implemenation up)
    """

    dir_name = "compressed_images"
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

    

# this is the name of the outputed compressed file. 
# This really could just be a random number
def compress(path_to_file):

    save_dir = gen_directory()
    
    dirs = os.listdir(path_to_file)
    for image in dirs:
        
        compressed_file = "compressed.jpeg"


        # take in a file named test.jpeg. this is hard to say
        im = Image.open(image)

        # dim is the size of im
        dim = im.size
        print(f"The image dimensions are: {dim}")       

        # find the size of the original file
        print(f"File size of the original file is: {os.stat(image).st_size}")

        # returns None
        im.save(save_dir + compressed_file, optimize=True, quality=30)


        pic = Image.open(compressed_file)
        print(f"The new image dimensions are: {pic.size}")
        print(f"the current directory: {os.getcwd()}")


