from PIL import Image
import os


# this is the name of the outputed compressed file. 
# This really could just be a random number
original_file = "FormatJPEG.jpeg"
compressed_file = "compressed.jpeg"



# take in a file named test.jpeg. this is hard to say
im = Image.open(original_file)

# dim is the size of im
dim = im.size
print(f"The image dimensions are: {dim}")

# find the size of the original file
print(f"File size of the original file is: {os.stat(original_file).st_size}")

# returns None
im.save(compressed_file, optimize=True, quality=30)


pic = Image.open(compressed_file)
print(f"The new image dimensions are: {pic.size}")
print(f"the current directory: {os.getcwd()}")



# Goals
# take more of a look at JS.
# look the RESTful APIs. Cuz i dont understand APIs that well.
# This will connect the user with our python file.
# Look the image.py file. we are going to see how they do the compression.
# goal is to grab all the images out of a file in the directory.
# Glob and pathlib