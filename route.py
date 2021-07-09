from PIL import Image
from flask import (
    Flask, 
    request,
    render_template)
import image_scrapper
import os

# hard code the name of the directory where the compressed images will end up.
static_dir = "static"

# Create Flask's `app` object
app = Flask(__name__)

@app.route("/", methods=["GET"])
def form():
    """
    Landing page. Simply take in an URL and quality value and ships to the download page
    """
    return render_template(
        'form.html'
    )

@app.route('/download', methods = ['POST', 'GET'])
def download():
    """
    Receive a URL from the landing page. Then scrape the website for its images, compress them, and display them. 
    I didn't worry about anything else.
    """

    if request.method == 'GET':
        return f"The URL /download was accessed directly. Try going to '/' to submit the URL first."
    if request.method == 'POST':
        # get the URL submited
        form_data = request.form
        url = form_data["URL"]
        quality = int(form_data["Quality"])

        # get the information about the website. a list of dictionaries
        # form: {url: , width: , height:}
        images_info = image_scrapper.get_images(url)
        # this will be sent to the html file to be displayed 

        # generate the directory to save the compressed images
        image_scrapper.gen_directory(static_dir)

        # compess and save the images. You can use uncompress to see which ones weren't in a format that could be compressed.
        # the names of the images that are compressed are saved to images_info dict
        uncompressed = image_scrapper.compress_images(images_info, static_dir, quality)
        # note that the images that can't be compressed are named 'x' which was dealt with in the template
        
        # get the names of the images
        dirs = os.listdir(static_dir)

        # probably could do some checks here but depends on how you want to implement it.
        return render_template('download.html', 
        form_data = form_data,
        image_info = images_info,
        image_names = dirs)


# quickly just run the app to start up the app. Not too much thought put into it.
app.run(host="0.0.0.0", debug=False)