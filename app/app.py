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
from dbAPI import get_course as db_get_course
from dbAPI import add_course as admin_add_course
from dbAPI import get_connection, get_user, get_all_courses, search_courses, get_course_averages, update_course
from dbAPI import get_reviews_for_course, upvote_review, downvote_review, flag_review, get_recent_reviews_for_user, get_recent_reviews, insert_review

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

    # retrieve username from the current session if user is logged in
    username = session.get("username")

    # retrieve the 5 most recent unflagged reviews
    reviews = get_recent_reviews(DATABASE_NAME, limit=5)

    return render_template("home.html", username=username, reviews=reviews)


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
    # process submitted login form
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        connection = get_connection(DATABASE_NAME)
        cursor = connection.cursor()

        # find user whose username and password match submitted values
        cursor.execute("SELECT * FROM Users WHERE username = ? AND password_hash = ?", (username, password))
        user = cursor.fetchone()

        connection.close()

        if user:
            # store the user's info in the session for future requests
            session["user_id"] = user["user_id"]
            session["username"] = user["username"]
            session["is_admin"] = user["is_admin"]

            # redirect user to homepage after successful login
            return redirect(url_for("home"))
        
        else:
            # reload ogin page when credentials don't match
            return render_template("login.html")
        
    # display the login form when the page is first loaded
    return render_template("login.html")


## SIGNUP - Display or process the signup form
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # add new user when signup form is submitted
    if request.method == 'POST':
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        connection = get_connection(DATABASE_NAME)
        cursor = connection.cursor()

        # insert new user's info into Users table
        cursor.execute("INSERT INTO Users (username, email, password_hash) VALUES (?, ?, ?)", (username, email, password))
        connection.commit()
        connection.close()

        # send new user to the login page
        return redirect(url_for("login"))
    
    else:
        return show_the_signup_form()

# Helper function to show the signup form
def show_the_signup_form():
    return render_template("signup.html")


## LOG OUT - Log the user out
@app.route('/logout')
def logout():
    # remove all saved login info from the session
    session.clear()

    return render_template("logout.html")


###############################################################################
## USER/ADMIN PROFILE ROUTES
###############################################################################

## USER PROFILE PAGE - display user's profile page with their info and reviews
@app.route('/profile')
def profile():

    # require the user to log in before accessing profile page
    if "user_id" not in session:
        return redirect(url_for("login"))

    # retrieve current user's info using the ID stored in the session
    user = get_user(DATABASE_NAME, session["user_id"])

    # retrieve the user's 5 most recent reviews for display on the profile page
    reviews = get_recent_reviews_for_user(DATABASE_NAME, session["user_id"], limit=5)
    
    return render_template(
        "profile.html",
        username=user["username"],
        email=user["email"],
        is_admin=user["is_admin"],
        reviews=reviews
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

        # update only the currently logged-in user's password
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


## ADMIN PANEL - display admin panel
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
    # retrieve submitted course info from form
    credits = int(request.form.get("credits"))
    course_name = request.form.get("course_name")
    course_code = request.form.get("course_code")
    description = request.form.get("description")
    course_type = request.form.get("course_type")

    # add the course and retrieve its newly created database ID
    course_id = admin_add_course(
        DATABASE_NAME,
        credits,
        course_name,
        course_code,
        description,
        course_type
    )

    # display the detail page for the newly created course
    return redirect(url_for("course_details", course_id=course_id))


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
    # retrieve the updated course info from the form
    credits = int(request.form.get("credits"))
    course_name = request.form.get("course_name")
    course_code = request.form.get("course_code")
    description = request.form.get("description")
    course_type = request.form.get("course_type")

    # update the matching course record in the database
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
        # return server error if database update failed
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
    # retrieve the course selected by its ID
    course = db_get_course(DATABASE_NAME, course_id)

    # return 404 page if course does not exist
    if course is None:
        abort(404)

    # retrieve the course's average scores and reviews
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

    # require login before allowing review to be submitted
    if "user_id" not in session:
        return redirect(url_for("login"))
   
    # retrieve text-based review fields. Need to validate these values
    review_text = request.form.get("review_text")
    semester = request.form.get("semester")

    # convert numeric form values from strings to integers
    try: 
        rating = int(request.form.get("rating"))
        difficulty = int(request.form.get("difficulty"))
        time = int(request.form.get("time"))
        year = int(request.form.get("year"))
    except (TypeError, ValueError) as error:
        return f"Invalid input: {error}"
 
    user_id = session["user_id"]

    # insert the review for the current user and selected course
    result = insert_review(DATABASE_NAME, course_id, user_id, review_text, rating, difficulty, time, year, semester)

    # redisplay the form with an error if the review could not be inserted
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
    # return to course page after successful submission
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
    # TO DO: Update the selected review in the database
    return f"do_edit_review called for course: {course_id}, review: {review_id}"

def show_edit_review_form(course_id, review_id):
    # TO DO: retrieve the existing review and populate the edit form
    return render_template("edit_review.html", course_id=course_id, review_id=review_id)


## UPVOTE REVIEW - increase a review's upvote count by 1
@app.route("/courses/<int:course_id>/reviews/<int:review_id>/upvote", methods=["POST"])

def upvote(course_id, review_id):

    if "user_id" not in session:
        return redirect(url_for("login"))
    
    review_found = upvote_review(DATABASE_NAME, review_id)

    if not review_found:
        abort(404)

    return redirect(url_for("course_details", course_id=course_id) + f"#review-{review_id}")

## DOWNVOTE REVIEW - increase a review's downvote count by one
@app.route("/courses/<int:course_id>/reviews/<int:review_id>/downvote", methods=["POST"]
)
def downvote(course_id, review_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    review_found = downvote_review(DATABASE_NAME, review_id)

    if not review_found:
        abort(404)

    return redirect(url_for("course_details", course_id=course_id) + f"#review-{review_id}")


## FLAG REVIEW - mark a review as flagged
@app.route(
    "/courses/<int:course_id>/reviews/<int:review_id>/flag",
    methods=["POST"]
)
def flag(course_id, review_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    review_found = flag_review(DATABASE_NAME, review_id)

    if not review_found:
        abort(404)

    return redirect(url_for("course_details", course_id=course_id) + f"#review-{review_id}")


###############################################################################

if __name__ == "__main__":
    app.run(debug=True)