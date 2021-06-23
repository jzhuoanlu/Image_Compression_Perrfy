from flask import Flask
from datetime import datetime

# learn decorators
# examples taken from https://realpython.com/primer-on-python-decorators/#first-class-objects
def say_hello(name):
    return f"Hello {name}"

def be_awesome(name):
    return f"Yo {name}, together we are the awesomest!"

def greet_bob(greeter_func):
    return greeter_func("Bob")

print(greet_bob(say_hello))
print("======================================================")
#inner function + return
def parent():
    print("Printing from the parent() function")

    def first_child():
        print("Printing from the first_child() function")

    def second_child():
        print("Printing from the second_child() function")

    return second_child()
    first_child()
parent()
print("======================================================")
def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

@my_decorator
def say_whee():
    print("Whee!")

# lol it seems that @my_decorator just replaces say_whee = my_decorator(say_whee)
# hmm there must be a reason we use this right? always its here now
say_whee()

#say_whee = my_decorator(say_whee)
# say_whee is wrapper() which is returned from my_decorator. func() prints "Whee!"
#say_whee()

# __name__ is a convenient shortcut for the name of hte application's module or package 
# tells flask where to look for resources such as templates and static files
#app = Flask(__name__)


# tells Flask what URL should trigger our function
#@app.route("/")

# returns message hello world to be displayed in HTML
#def hello_world():
#    return "<p>Hello, World!</p>"