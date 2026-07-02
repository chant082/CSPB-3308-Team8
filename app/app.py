###############################################################################
## This is the backend for the CSPB Course Review Platform application
##
## CSPB 3308 Summer 2026
## Author: Team 8 (Hannah Pfeifer, Adam Chathankeo, Craig Sanders, Sean Lin)
## Date: 7/1/26
##
###############################################################################

from flask import Flask, url_for, request, render_template 
from markupsafe import escape

# Create the Flask application
app = Flask(__name__)

###############################################################################
## Routes

## HOMEPAGE (Guest view)
@app.route("/")
def home():
    return "<h1>Welcome to the CSPB Course Review Platform</h1>"
# need header(logo), log in/register link, about link/index(footer), search bar, browse link, etc. (all links will be implemented later)

## HOMEPAGE (Logged in view)
@app.route("/welcome/<username>")
def user(username):
    return "<h1>Welcome, {}!</h1>".format(escape(username))

## NAVIGATION PAGE (Guest view) contains links to all pages in the application
@app.route('/navigation')
def navigation():
    return """
    <h1>Website Navigation</h1>
    <ul>
        <li>/</li>
        <li>/about</li>
        <li>/login</li>
        <li>/profile/&lt;username&gt;</li>
    </ul>
    """
## add more later as we add pages

## ABOUT PAGE
@app.route('/about')
def about():
    return """
    <h1>About</h1>
    <p>Team #: 8</p>
    <p>ADD WEBSITE DESCRIPTION</p>
    """

## LOGIN ROUTES
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()
        
def show_the_login_form():
    return "show_the_login_form called"

def do_the_login():
    return "do_the_login called"

## USER PROFILE PAGE
@app.route('/profile/<username>')
def profile(username):   
    # show the user profile for that user
    return f"User {escape(username)}'s profile"
# if guest somehow ends up here, redirect to login page


###############################################################################
## Future Routes
##
## - Course search
## - Browse courses
## - Course details
## - Submit review
## - Edit review
## - Student profile
## - Admin profile/dashboard
## - Registration
## - Logout
###############################################################################

if __name__ == "__main__":
    app.run(debug=True)