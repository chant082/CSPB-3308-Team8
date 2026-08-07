###############################################################################
## Backend for the CSPB Course Review Platform using Flask.
##
## CSPB 3308 Summer 2026
## Author: Team Infinity(Team 8): Hannah Pfeifer, Adam Chathankeo, Craig Sanders, Sean Lin
## Date: 7/1/26
##
###############################################################################

from flask import Flask, session, url_for, request, render_template, redirect, abort
from markupsafe import escape
from create_db import DATABASE_NAME
from dbAPI import get_course as db_get_course
from dbAPI import add_course as admin_add_course
from dbAPI import get_connection, get_user, get_all_users, get_all_courses, search_courses, get_course_averages, update_course
from dbAPI import get_reviews_for_course, upvote_review, downvote_review, flag_review, get_recent_reviews_for_user, get_recent_reviews, insert_review
from dbAPI import get_review, update_review, get_review_by_user_and_course, get_flagged_reviews

from datetime import datetime
current_year = datetime.now().year

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

    # Retrieve username from the current session if user is logged in
    username = session.get("username")

    # Retrieve the 5 most recent unflagged reviews
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
@app.route('/login', methods=["GET", "POST"])
def login():
    # Process submitted login form
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        connection = get_connection(DATABASE_NAME)
        cursor = connection.cursor()

        # Find user whose username and password match submitted values
        cursor.execute("SELECT * FROM Users WHERE username = ? AND password_hash = ?", (username, password))
        user = cursor.fetchone()

        connection.close()

        if user:
            # Store the user's info in the session for future requests
            session["user_id"] = user["user_id"]
            session["username"] = user["username"]
            session["is_admin"] = user["is_admin"]

            # Redirect user to homepage after successful login
            return redirect(url_for("home"))
        
        else:
            return render_template(
                "login.html",
                error="Invalid username or password."
            )
        
    # Display the login form when the page is first loaded
    return render_template("login.html")


## SIGNUP - Display or process the signup form
@app.route('/signup', methods=["GET", "POST"])
def signup():

    if request.method == "POST":
        username = request.form["username"].strip()
        email = request.form["email"].strip()
        password = request.form["password"]

        connection = get_connection(DATABASE_NAME)
        cursor = connection.cursor()

        # Check password length
        if len(password) < 8:
            connection.close()
            return render_template("signup.html", error="Password must be at least 8 characters long.")

        # Check username
        cursor.execute(
            "SELECT 1 FROM Users WHERE username = ?",
            (username,)
        )

        if cursor.fetchone():
            connection.close()
            return render_template("signup.html", error="Username is already taken.")

        # Check email domain
        if not email.endswith("@colorado.edu"):
            connection.close()
            return render_template("signup.html", error="Please use a valid @colorado.edu email address.")

        # Check email
        cursor.execute(
            "SELECT 1 FROM Users WHERE email = ?",
            (email,)
        )

        if cursor.fetchone():
            connection.close()
            return render_template("signup.html", error="An account with that email already exists.")

        # Create new user account
        cursor.execute(
            "INSERT INTO Users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, password)
        )

        connection.commit()
        connection.close()

        return redirect(url_for("login"))

    return show_the_signup_form()

# Helper function to show the signup form
def show_the_signup_form():
    return render_template("signup.html")


## LOG OUT - Log the user out
@app.route('/logout')
def logout():
    # Remove all saved login info from the session
    session.clear()

    return render_template("logout.html")


###############################################################################
## USER/ADMIN PROFILE ROUTES
###############################################################################


## USER PROFILE PAGE - display user's profile page with their info and reviews
@app.route('/profile')
def profile():

    # Require the user to log in before accessing profile page
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Retrieve current user's info using the ID stored in the session
    user = get_user(DATABASE_NAME, session["user_id"])

    # Retrieve the user's 5 most recent reviews for display on the profile page
    reviews = get_recent_reviews_for_user(DATABASE_NAME, session["user_id"], limit=5)
    
    return render_template("profile.html",
        username=user["username"],
        email=user["email"],
        is_admin=user["is_admin"],
        reviews=reviews
    )


## USER UPDATE INFO - display or process the update info form
@app.route('/profile/update_info', methods=["GET", "POST"])
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

        # Check password length
        if len(password) < 8:
            return show_update_info_form(
                error="Password must be at least 8 characters long."
            )

        connection = get_connection(DATABASE_NAME)
        cursor = connection.cursor()

        # Update only the currently logged-in user's password
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


def show_update_info_form(error=None):
    user = get_user(DATABASE_NAME, session["user_id"])

    return render_template("user_update_info.html",
        username=user["username"],
        email=user["email"],
        error=error
    )


## ADMIN PANEL - display admin panel
@app.route('/admin/<username>')
def admin(username):
    courses = get_all_courses(DATABASE_NAME)
    users = get_all_users(DATABASE_NAME)
    flagged_reviews = get_flagged_reviews(DATABASE_NAME)

    return render_template("admin_panel.html", 
        username=escape(username), 
        courses=courses,
        users=users,
        flagged_reviews=flagged_reviews
        )


## ADMIN ADD COURSE - display or process the add course form
@app.route('/admin/<username>/add_course', methods=["GET", "POST"])
def add_course(username):
    if request.method == "POST":
        return do_add_course(username)
    else:
        return show_add_course_form(username)

def do_add_course(username):
    # Retrieve submitted course info from form
    credits = int(request.form.get("credits"))
    course_name = request.form.get("course_name")
    course_code = request.form.get("course_code")
    description = request.form.get("description")
    course_type = request.form.get("course_type")

    # Add the course and retrieve its newly created database ID
    course_id = admin_add_course(
        DATABASE_NAME,
        credits,
        course_name,
        course_code,
        description,
        course_type
    )

    # Display the detail page for the newly created course
    return redirect(url_for("course_details", course_id=course_id))


def show_add_course_form(username):
    return render_template("admin_add_course.html", username=username)


## ADMIN EDIT COURSE - Display or process the edit course form
@app.route('/admin/<username>/edit_course/<int:course_id>', methods=["GET", "POST"])
def edit_course(username, course_id):
    if request.method == "POST":
        return do_edit_course(username, course_id)
    else:
        return show_edit_course_form(username, course_id)

def do_edit_course(username, course_id):
    # Retrieve the updated course info from the form
    credits = int(request.form.get("credits"))
    course_name = request.form.get("course_name")
    course_code = request.form.get("course_code")
    description = request.form.get("description")
    course_type = request.form.get("course_type")

    # Update the matching course record in the database
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
        # Return server error if database update failed
        return "The course could not be updated.", 500

    return redirect(
        url_for("course_details", course_id=course_id)
    )


def show_edit_course_form(username, course_id):
    course = db_get_course(DATABASE_NAME, course_id)

    if course is None:
        abort(404)

    return render_template("admin_edit_course.html",
        username=username,
        course=course
    )


###############################################################################
## COURSE ROUTES
###############################################################################


## BROWSE/SEARCH COURSES - display all courses or process a course search
@app.route('/courses', methods=["GET", "POST"])
def browse_courses():
    if request.method == "POST":
        return do_search_courses()
    else:
        return show_courses()   


# Search for courses by keyword. If no keyword entered, display all courses
def do_search_courses():

    # Get the search keyword entered by user and remove any leading or trailing whitespace
    keyword = request.form.get("keyword", "").strip()

    # Search DB if a keyword was entered. Otherwise retrieve all courses
    if keyword:
        courses = search_courses(DATABASE_NAME, keyword)
    else:
        courses = get_all_courses(DATABASE_NAME)

    # Create new list that includes course info and average review stats
    course_list = []

    # Add average rating, difficulty, and workload to each course
    for course in courses:
        course_data = dict(course)

        averages = get_course_averages(DATABASE_NAME, course["course_id"])

        course_data["avg_rating"] = averages["avg_rating"]
        course_data["avg_difficulty"] = averages["avg_difficulty"]
        course_data["avg_workload"] = averages["avg_workload"]

        course_list.append(course_data)

    # Display matching courses
    return render_template("courses.html", courses = course_list, keyword = keyword)    


# Display all courses
def show_courses():

    # Get all courses from database
    courses = get_all_courses(DATABASE_NAME)

    # Create a new list that includes course info and average review stats
    course_list = []

    # Add average rating, difficulty, and workload to each course
    for course in courses:
        course_data = dict(course)

        averages = get_course_averages(DATABASE_NAME, course["course_id"])

        course_data["avg_rating"] = averages["avg_rating"]
        course_data["avg_difficulty"] = averages["avg_difficulty"]
        course_data["avg_workload"] = averages["avg_workload"]

        course_list.append(course_data)

    # Display all courses
    return render_template("courses.html", courses = course_list)


## COURSE DETAILS - display the details of a specific course and its reviews
@app.route('/courses/<int:course_id>')
def course_details(course_id):
    # Retrieve the course selected by its ID
    course = db_get_course(DATABASE_NAME, course_id)

    # Return 404 page if course does not exist
    if course is None:
        abort(404)

    # Retrieve the course's average scores and reviews
    averages = get_course_averages(DATABASE_NAME, course_id)
    reviews = get_reviews_for_course(DATABASE_NAME, course_id)
    
    return render_template("course_details.html", course=course, averages=averages, reviews=reviews)


###############################################################################
## REVIEW ROUTES
###############################################################################


## SUBMIT REVIEW - display or process the submit review form for a specific course
@app.route('/courses/<int:course_id>/submit_review', methods=['GET', 'POST'])
def submit_review(course_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    existing_review = get_review_by_user_and_course(
        DATABASE_NAME,
        session["user_id"],
        course_id
    )

    if existing_review is not None:
        return redirect(
            url_for("edit_review",
                course_id=course_id,
                review_id=existing_review["review_id"]
            )
        )
    
    if request.method == "POST":
        return do_submit_review(course_id)

    return show_submit_review_form(course_id)


def do_submit_review(course_id):

    # Require login before allowing review to be submitted
    if "user_id" not in session:
        return redirect(url_for("login"))
   
    # Retrieve text-based review fields. Need to validate these values
    review_text = request.form.get("review_text")
    semester = request.form.get("semester")

    # Convert numeric form values from strings to integers
    try: 
        rating = int(request.form.get("rating"))
        difficulty = int(request.form.get("difficulty"))
        time = int(request.form.get("time"))
        year = int(request.form.get("year"))
    except (TypeError, ValueError) as error:
        return f"Invalid input: {error}"
 
    user_id = session["user_id"]

    # Insert the review for the current user and selected course
    result = insert_review(DATABASE_NAME, course_id, user_id, review_text, rating, difficulty, time, year, semester)

    # Redisplay the form with an error if the review could not be inserted
    if result != "review insertion successful.": 
        error = "You have already submitted a review for this course." if result == "duplicate" else "An error occurred submitting your review"

        course = db_get_course(DATABASE_NAME, course_id)
        return render_template("submit_review.html",
            course_id=course_id,
            course=course,
            error=error,
            form=request.form,
            current_year=datetime.now().year
        )
    # Return to course page after successful submission
    return redirect(url_for('course_details', course_id=course_id))


def show_submit_review_form(course_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    course = db_get_course(DATABASE_NAME, course_id)
    return render_template(
        "submit_review.html", 
        course_id = course_id, 
        course = course,
        current_year=current_year)


## EDIT REVIEW - display or process the edit review form for a specific course and review
@app.route('/courses/<int:course_id>/edit_review/<int:review_id>', methods=['GET', 'POST'])
def edit_review(course_id, review_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        return do_edit_review(course_id, review_id)

    return show_edit_review_form(course_id, review_id)


def do_edit_review(course_id, review_id):

    review_text = request.form.get("review_text")
    semester = request.form.get("semester")

    try:
        rating = int(request.form.get("rating"))
        difficulty = int(request.form.get("difficulty"))
        workload = int(request.form.get("workload"))
        year = int(request.form.get("year"))

    except (TypeError, ValueError):
        return "Invalid numeric input.", 400

    success = update_review(
        DATABASE_NAME,
        review_id,
        review_text,
        rating,
        difficulty,
        workload,
        year,
        semester
    )

    if not success:
        return "The review could not be updated.", 500

    return redirect(
        url_for("course_details", course_id=course_id)
        + f"#review-{review_id}"
    )

def show_edit_review_form(course_id, review_id):
    review = get_review(DATABASE_NAME, review_id)

    return render_template(
        "edit_review.html",
        review=review,
        current_year=datetime.now().year
    )



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
