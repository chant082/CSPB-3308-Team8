###############################################################################
## Backend for the CSPB Course Review Platform using Flask.
##
## CSPB 3308 Summer 2026
## Author: Team 8 - Team Infinity: Hannah Pfeifer, Adam Chathankeo, Craig Sanders, Sean Lin
## Date: 7/1/26
##
###############################################################################


from flask import Flask, url_for, request, render_template 
from markupsafe import escape

# Create the Flask application
app = Flask(__name__)


###############################################################################
## HOMEPAGE AND GENERAL WEBSITE ROUTES
###############################################################################

## HOMEPAGE (GUEST)
@app.route('/')
def home():
    return render_template("home.html", username=None)


## HOMEPAGE (USER)
@app.route('/home/<username>')
def user_home(username):
    return render_template("home.html", username=escape(username))


## ABOUT PAGE
@app.route('/about')
def about():
    return render_template("about.html")


###############################################################################
## LOGIN AND SIGNUP ROUTES
###############################################################################

## LOGIN - Display or process the login form
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()

def do_the_login():
    return "do_the_login called."

def show_the_login_form():
    return render_template("login.html")


## SIGNUP - Display or process the signup form
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        return do_the_signup()
    else:
        return show_the_signup_form()
    
def do_the_signup():
    return "do_the_signup called."

def show_the_signup_form():
    return render_template("signup.html")
    
## LOG OUT - Log the user out and redirect to the homepage
@app.route('/logout')
def logout():
    return "logout called."

###############################################################################
## USER/ADMIN PROFILE ROUTES
###############################################################################

## NORMAL USER PROFILE PAGE - display user's profile page with their info and reviews
@app.route('/profile/<username>')
def profile(username):   
    return render_template("profile.html", username=escape(username))


## USER UPDATE INFO - display or process the update info form
@app.route('/profile/<username>/update_info', methods=['GET', 'POST'])
def update_info(username):
    if request.method == 'POST':
        return do_update_info(username)
    else:
        return show_update_info_form(username)

def do_update_info(username):
    return f"do_update_info called for user: {username}"

def show_update_info_form(username):
    return render_template("user_update_info.html", username=escape(username))


## ADMIN PROFILE - display the admin panel
@app.route('/admin/<username>')
def admin(username):
    return render_template("admin_panel.html", username=escape(username))


## ADMIN ADD COURSE - display or process the add course form
@app.route('/admin/<username>/add_course', methods=['GET', 'POST'])
def add_course(username):
    if request.method == 'POST':
        return do_add_course(username)
    else:
        return show_add_course_form()

def do_add_course(username):
    return f"do_add_course called for user: {username}"

def show_add_course_form():
    return render_template("admin_add_course.html")


## ADMIN EDIT COURSE - Display or process the edit course form
@app.route('/admin/<username>/edit_course/<int:course_id>', methods=['GET', 'POST'])
def edit_course(username, course_id):
    if request.method == 'POST':
        return do_edit_course(course_id)
    else:
        return show_edit_course_form(course_id)

def do_edit_course(course_id):
    return f"do_edit_course called for course: {course_id}"

def show_edit_course_form(course_id):
    return render_template("admin_edit_course.html", course_id=course_id)


###############################################################################
## COURSE ROUTES
###############################################################################

## BROWSE/SEARCH COURSE - display all courses or process a course search
@app.route('/courses', methods=['GET', 'POST'])
def browse_courses():
    if request.method == 'POST':
        return do_search_courses()
    else:
        return show_courses()   

def do_search_courses():
    return "do_search_courses called"       

def show_courses():
    return render_template("courses.html")


## COURSE DETAILS - display the details of a specific course and its reviews
@app.route('/courses/<int:course_id>')
def course_details(course_id):
    return render_template("course_details.html", course_id=escape(course_id))  


###############################################################################
## REVIEW ROUTES
###############################################################################

## SUBMIT REVIEW - display or process the submit review form for a specific course
@app.route('/courses/<int:course_id>/submit_review', methods=['GET', 'POST'])
def submit_review(course_id):
    if request.method == 'POST':
        return do_submit_review(course_id)
    else:
        return show_submit_review_form(course_id)

def do_submit_review(course_id):
    return f"do_submit_review called for course: {course_id}"

def show_submit_review_form(course_id):
    return render_template("submit_review.html", course_id=course_id)

## EDIT REVIEW - display or process the edit review form for a specific course and review
@app.route('/courses/<int:course_id>/edit_review/<int:review_id>', methods=['GET', 'POST'])
def edit_review(course_id, review_id):
    if request.method == 'POST':
        return do_edit_review(course_id, review_id)
    else:
        return show_edit_review_form(course_id, review_id)

def do_edit_review(course_id, review_id):
    return f"do_edit_review called for course: {course_id}, review: {review_id}"

def show_edit_review_form(course_id, review_id):
    return render_template("edit_review.html", course_id=course_id, review_id=review_id)


###############################################################################

if __name__ == "__main__":
    app.run(debug=True)