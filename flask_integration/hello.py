from flask import Flask, url_for

app = Flask(__name__)

from flask import request


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()

def do_the_login():
   return 'Logged in!'

def show_the_login_form():
   return 'Login form:'
