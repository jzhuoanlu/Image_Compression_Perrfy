from flask import (
    Flask, 
    request,
    render_template)
import image_scrapper
import os

save_dir = "static/images"
compress_dir = "static/compressed_images"

# Create Flask's `app` object
app = Flask(__name__)

# this will be my landing page for now.
@app.route("/", methods=["GET", "POST"])
def form():
    return render_template(
        'form.html'
    )

@app.route('/download', methods = ['POST', 'GET'])
def download():
    if request.method == 'GET':
        return f"The URL /download is accessed directly. Try going to '/' to submit form"
    if request.method == 'POST':
        form_data = request.form

        # retrieve the entered url
        url = form_data["URL"]

        # get the image source url
        images = image_scrapper.get_images(url)
        
        image_scrapper.gen_directory(save_dir)
        # download the images to local file. This might change but will sufice for now.
        image_scrapper.download_images(url, images, save_dir)
        


        # ***** incomplete *****
        # get the number of images found to be displayed
        num_images = str(len(images))
        # get the names of the images
        dirs = os.listdir(save_dir)
        # probably should do some checks here but we worry about that later.

        # i'm currently having a hard time getting the images to render. something about the static folder
        return render_template('download.html', 
        form_data = form_data,
        num_images = num_images,
        image_names = dirs)

@app.route('/compressed', methods = ['POST', 'GET'])
def test():
    if request.method == 'GET':
        image_scrapper.gen_directory(compress_dir)
        image_scrapper.compress(save_dir, compress_dir)
        return render_template('compressed.html')
    

app.run(host="0.0.0.0", debug=False)