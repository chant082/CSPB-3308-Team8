###############################################################################
## Backend for the CSPB Course Review Platform using Flask.
##
## CSPB 3308 Summer 2026
## Author: Team 8 - Team Infinity: Hannah Pfeifer, Adam Chathankeo, Craig Sanders, Sean Lin
## Date: 7/1/26
##
###############################################################################

from getpass import getuser

from flask import Flask, session, url_for, request, render_template, redirect, abort
from markupsafe import escape
from create_db import DATABASE_NAME
from dbAPI import get_course as db_get_course, get_user
from dbAPI import get_connection, get_all_courses, search_courses, get_course_averages, get_reviews_for_course
from dbAPI import add_course as admin_add_course
from dbAPI import update_course, insert_review

# Create the Flask application
app = Flask(__name__)

# Set a secret key for session management. In a real application, this should be a secure random value and kept secret.
app.secret_key = "CSPB3308Team8"

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
## LOGIN, LOGOUT, AND SIGNUP ROUTES
###############################################################################

## LOGIN - Display or process the login form
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        connection = get_connection(DATABASE_NAME)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Users WHERE username = ? AND password_hash = ?", (username, password))
        user = cursor.fetchone()

        connection.close()
        if user:
            session["user_id"] = user["user_id"]
            session["username"] = user["username"]
            session["is_admin"] = user["is_admin"]

            return redirect(url_for("user_home", username=user["username"]))
        else:
            return render_template(
                "login.html"
            )
    return render_template("login.html")


## SIGNUP - Display or process the signup form
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        connection = get_connection(DATABASE_NAME)
        cursor = connection.cursor()

        cursor.execute("INSERT INTO Users (username, email, password_hash) VALUES (?, ?, ?)", (username, email, password))
        connection.commit()
        connection.close()

        return redirect(url_for("login"))
    
    else:
        return show_the_signup_form()

#Helpful function to show the signup form
def show_the_signup_form():
    return render_template("signup.html")
    
## LOG OUT - Log the user out and redirect to the homepage
@app.route('/logout')
def logout():
    session.clear()
    return render_template("logout.html")

###############################################################################
## USER/ADMIN PROFILE ROUTES
###############################################################################

## NORMAL USER PROFILE PAGE - display user's profile page with their info and reviews
@app.route('/profile')
def profile():
    if "user_id" not in session:
        return redirect(url_for("login"))

    #Import the get_user function from dbAPI.py and use it to retrieve the user's information from the database using their user_id stored in the session.
    user = get_user(DATABASE_NAME, session["user_id"])

    return render_template(
        "profile.html",
        username=user["username"],
        email=user["email"],
        is_admin=user["is_admin"]
    )


## USER UPDATE INFO - display or process the update info form
@app.route('/profile/update_info', methods=['GET', 'POST'])
def update_info():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        return do_update_info()

    return show_update_info_form()

def do_update_info():
    connection = None

    try:
        password = request.form["password"]

        connection = get_connection(DATABASE_NAME)
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE Users
            SET password_hash = ?
            WHERE user_id = ?
        """, (password, session["user_id"]))

        connection.commit()

    finally:
        if connection is not None:
            connection.close()

    return redirect(url_for("profile"))

def show_update_info_form():
    user = get_user(DATABASE_NAME, session["user_id"])

    return render_template(
        "user_update_info.html",
        username=user["username"],
        email=user["email"]
    )


## ADMIN PROFILE - display the admin panel
@app.route('/admin/<username>')
def admin(username):
    courses = get_all_courses(DATABASE_NAME)
    return render_template("admin_panel.html", username=escape(username), courses=courses)


## ADMIN ADD COURSE - display or process the add course form
@app.route('/admin/<username>/add_course', methods=['GET', 'POST'])
def add_course(username):
    if request.method == 'POST':
        return do_add_course(username)
    else:
        return show_add_course_form(username)

def do_add_course(username):
    credits = int(request.form.get("credits"))
    course_name = request.form.get("course_name")
    course_code = request.form.get("course_code")
    description = request.form.get("description")
    course_type = request.form.get("course_type")

    course_id = admin_add_course(
        DATABASE_NAME,
        credits,
        course_name,
        course_code,
        description,
        course_type
    )

    return redirect(
        url_for("course_details", course_id=course_id)
    )

def show_add_course_form(username):
    return render_template("admin_add_course.html", username=username)


## ADMIN EDIT COURSE - Display or process the edit course form
@app.route('/admin/<username>/edit_course/<int:course_id>', methods=['GET', 'POST'])
def edit_course(username, course_id):
    if request.method == 'POST':
        return do_edit_course(username, course_id)
    else:
        return show_edit_course_form(username, course_id)

def do_edit_course(username, course_id):
    credits = int(request.form.get("credits"))
    course_name = request.form.get("course_name")
    course_code = request.form.get("course_code")
    description = request.form.get("description")
    course_type = request.form.get("course_type")

    success = update_course(
    DATABASE_NAME,
    course_id,
    credits,
    course_name,
    course_code,
    description,
    course_type
    )

    if not success:
        return "The course could not be updated.", 500

    return redirect(
        url_for("course_details", course_id=course_id)
    )

def show_edit_course_form(username, course_id):
    course = db_get_course(DATABASE_NAME, course_id)

    if course is None:
        abort(404)

    return render_template(
        "admin_edit_course.html",
        username=username,
        course=course
    )


###############################################################################
## COURSE ROUTES
###############################################################################

## BROWSE/SEARCH COURSES - display all courses or process a course search
@app.route('/courses', methods=['GET', 'POST'])
def browse_courses():
    if request.method == 'POST':
        return do_search_courses()
    else:
        return show_courses()   


# search for courses by keyword. If no keyword entered, display all courses
def do_search_courses():

    # get the search keyword entered by user and remove any leading or trailing whitespace
    keyword = request.form.get("keyword", "").strip()

    # search DB if a keyword was entered. Otherwise retrieve all courses
    if keyword:
        courses = search_courses(DATABASE_NAME, keyword)
    else:
        courses = get_all_courses(DATABASE_NAME)

    # create new list that includes course info and average review stats
    course_list = []

    # add average rating, difficulty, and workload to each course
    for course in courses:
        course_data = dict(course)

        averages = get_course_averages(DATABASE_NAME, course["course_id"])

        course_data["avg_rating"] = averages["avg_rating"]
        course_data["avg_difficulty"] = averages["avg_difficulty"]
        course_data["avg_workload"] = averages["avg_workload"]

        course_list.append(course_data)

    # display matching courses
    return render_template("courses.html", courses = course_list, keyword = keyword)    

# display all courses
def show_courses():

    # get all courses from database
    courses = get_all_courses(DATABASE_NAME)

    # create a new list that includes course info and average review stats
    course_list = []

    # add average rating, difficulty, and workload to each course
    for course in courses:
        course_data = dict(course)

        averages = get_course_averages(DATABASE_NAME, course["course_id"])

        course_data["avg_rating"] = averages["avg_rating"]
        course_data["avg_difficulty"] = averages["avg_difficulty"]
        course_data["avg_workload"] = averages["avg_workload"]

        course_list.append(course_data)

    # display all courses
    return render_template("courses.html", courses = course_list)


## COURSE DETAILS - display the details of a specific course and its reviews
@app.route('/courses/<int:course_id>')
def course_details(course_id):
    course = db_get_course(DATABASE_NAME, course_id)

    if course is None:
        abort(404)

    averages = get_course_averages(DATABASE_NAME, course_id)
    reviews = get_reviews_for_course(DATABASE_NAME, course_id)
    
    return render_template("course_details.html", course=course, averages=averages, reviews=reviews)


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
   
    #need to validate these values
    review_text = request.form.get("review_text")
    semester = request.form.get("semester")
    try: 
        rating = int(request.form.get("rating"))
        difficulty = int(request.form.get("difficulty"))
        time = int(request.form.get("time"))
        year = int(request.form.get("year"))
    except ValueError as ve:
        return f"Invalid input: {ve}"
 
    if "user_id" not in session:
            return redirect(url_for("login"))

    user_id = session["user_id"]

    result = insert_review(DATABASE_NAME, course_id, user_id, review_text, rating, difficulty, time, year, semester)

    if result != "review insertion successful.": 
        error = "You have already submitted a review for this course." if result == "duplicate" else "An error occurred submitting your review"

        course = db_get_course(DATABASE_NAME, course_id)
        return render_template(
            "submit_review.html",
            course_id=course_id,
            course=course,
            error=error,
            form=request.form,
        )
    return redirect(url_for('course_details', course_id=course_id))

def show_submit_review_form(course_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    course = db_get_course(DATABASE_NAME, course_id)
    return render_template("submit_review.html", course_id = course_id, course = course)

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