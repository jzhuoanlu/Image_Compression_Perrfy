from flask import (
    Flask, 
    request,
    render_template)
import image_scrapper
import os


# Create Flask's `app` object
app = Flask(__name__)

# this will be my landing page for now.
@app.route("/", methods=["GET", "POST"])
def form():
    return render_template(
        'form.html'
    )

@app.route('/data/', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form

        # retrieve the entered url
        url = form_data["URL"]

        # get the image source url
        images = image_scrapper.get_images(url)
        
        saved_images = image_scrapper.gen_directory()
        # download the images to local file. This might change but will sufice for now.
        image_scrapper.download_images(url, images, saved_images)
        


        # ***** incomplete *****
        # get the number of images found to be displayed
        num_images = str(len(images))
        # get the names of the images
        dirs = os.listdir(saved_images)

        # probably should do some checks here but we worry about that later.

        # i'm currently having a hard time getting the images to render. something about the static folder
        return render_template('data.html', 
        form_data = form_data,
        num_images = num_images,
        image_urls = dirs)


app.run(host="0.0.0.0", debug=False)