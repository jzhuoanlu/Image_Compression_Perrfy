from flask import (
    Flask, 
    request,
    render_template)
import image_scrapper
import os

# hard code the name of the directory where the compressed images will end up.
static_dir = "static"
compress_dir = "static/compressed_images"

# Create Flask's `app` object
app = Flask(__name__)

@app.route("/", methods=["GET"])
def form():
    """
    Landing page. Simply take in an URL and ships to the download page
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

        # get the image source urls off the submitted websites
        image_urls = image_scrapper.get_image_urls(url)

        # generate the directory to save the compressed images
        image_scrapper.gen_directory(static_dir)
        # generate the directory to save the compressed images
        image_scrapper.gen_directory(compress_dir)

        # compess and save the images. You can use uncompress to see which ones weren't in a format that could be compressed.
        uncompressed = image_scrapper.compress_images(image_urls, compress_dir, quality)
        
        # get the names of the images
        dirs = os.listdir(compress_dir)
        # probably should do some checks here but we worry about that later.

        return render_template('download.html', 
        form_data = form_data,
        image_names = dirs)

app.run(host="0.0.0.0", debug=False)