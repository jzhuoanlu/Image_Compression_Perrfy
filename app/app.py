from flask import (
    Flask, 
    Markup, 
    make_response, 
    request, 
    jsonify)
from flask.templating import render_template
from forms import ContactForm
from logic import square_of_number_plus_nine


# Create Flask's `app` object
app = Flask(__name__)

# this will be my landing page for now.
@app.route("/", methods=["GET", "POST"])
def home():
    #value = square_of_number_plus_nine(5)
    #return value
    #return Markup(f"<h1>{square_of_number_plus_nine(5)}</h1>")
    #headers = {"Contest-Type": "application/json"}
    #return make_response('it worked!', 200, headers)

    """
    if request.method != 'GET':
        return make_response('Malformed request', 400)
    """

    """this is the dictionary that is "jsonifyed" into something to be displayed
    still dont know what exactly what hte point of the headers are. 
    my_dict = {'key': 'dictionary value', 'testkey': 'testvalue'}
    headers = {"Content-Type": "application/json"}
    return make_response(jsonify(my_dict), 200, headers)"""

    form = ContactForm()
    if form.validate_on_submit():
        return redirect(url_for("success"))
    

    return render_template(
        'home.html',
        title="demo template",
        description="try this instead of the Markup shit from before."
    )