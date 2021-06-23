import os

from flask import Flask



# Note PAIN. this tutorial is pain. apperently, the flask api tutorial is pretty bad, so im to to try and switch for now.
# but i will be back. im going on my training arc and I shall return

# application factory function
# what is a application function 
# refers to a common "pattern" to solve the problem of importing the app object all over the place.
# Flask's application context. takes python files and modules that make up our app and brings them together
# 
def create_app(test_config=None):
    # create and configure the app
    # note instance folder is designed not to be under version control and be deployment specific
    app = Flask(__name__, instance_relative_config=True)

    # dev is a convenitent value during development but it should be overridden with a random value when depolying
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # a simple page that says hello
    # create a route? what is a route? apperently it is a decorator what is that?
    # a decorator is a function that takes another fuctnion and extends the behavior without modifying it?
    
    # router tells the application which URL should call the function.
    # i guess this decorator takes in the hello method as an input and runs it.
    @app.route('/hello')
    def hello():
        return 'Hello, Worldtest!'

    # create the database. 
    from . import db
    db.init_app(app)

    return app
