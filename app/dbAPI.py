# CSPB 3308
# CSPB Course Review Platform

# This Python script provides some useful methods
# for retriving data or inserting data

import sqlite3

# create and return a database connection
# sqlite3.Row enables you to access specific data by column name
def get_connection(db_name):

    connection = sqlite3.connect(db_name)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


# return a list of all courses
# sorted by course code

# usage: use a for loop to iterate course.
""" 
Example

for course in courses:  
    print(course["course_code"])
    print(course["course_name"])
"""

def get_all_courses(db_name):

    connection = None

    try:
        connection = get_connection(db_name)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM Courses
            ORDER BY course_code;
        """)

        courses = cursor.fetchall()

        return courses

    finally:
        if connection is not None:
            connection.close()



# return one course with a course ID
# return None if the course ID does not exist

# usage: use column names as indices to access specific data
# for example - course["course_name"] or course["course_code"]

def get_course(db_name, course_id):

    connection = None

    try:
        connection = get_connection(db_name)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM Courses
            WHERE course_id = ?;
        """, (course_id,))

        course = cursor.fetchone()

        return course

    finally:
        if connection is not None:
            connection.close()


# search for courses whose name or code contains the keyword
# return a list of courses that match criteria
def search_courses(db_name, keyword):

    connection = None

    try:
        connection = get_connection(db_name)
        cursor = connection.cursor()

        search_pattern = "%" + keyword + "%"

        cursor.execute("""
            SELECT *
            FROM Courses
            WHERE course_code LIKE ?
               OR course_name LIKE ?
            ORDER BY course_code;
        """, (search_pattern, search_pattern))

        courses = cursor.fetchall()

        return courses

    finally:
        if connection is not None:
            connection.close()


# return the average rating, difficulty, and workload of a course
def get_course_averages(db_name, course_id):

    connection = None

    try:
        connection = get_connection(db_name)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                COALESCE(AVG(rating), 0) AS avg_rating,
                COALESCE(AVG(difficulty), 0) AS avg_difficulty,
                COALESCE(AVG(workload), 0) AS avg_workload
            FROM Reviews
            WHERE course_id = ?
        """, (course_id,))

        averages = cursor.fetchone()

        return averages

    finally:
        if connection is not None:
            connection.close()




# update a course
# return true if successful and false if failed
def update_course(
    db_name,
    course_id,
    credits,
    course_name,
    course_code,
    description,
    course_type
):
    connection = None

    try:
        connection = get_connection(db_name)
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE Courses
            SET credits = ?,
                course_name = ?,
                course_code = ?,
                description = ?,
                course_type = ?
            WHERE course_id = ?
            """,
            (
                credits,
                course_name,
                course_code,
                description,
                course_type,
                course_id
            )
        )

        connection.commit()

        return cursor.rowcount > 0

    except sqlite3.Error as error:
        if connection is not None:
            connection.rollback()

        print(f"Error updating course: {error}")
        return False

    finally:
        if connection is not None:
            connection.close()


# return all reviews for one course
# this contains reviews themselves and the usernames of authors

# usage: use a loop to iterate reviews
"""
For Example

for review in reviews:
    print(review["username"])
    print(review["review_text"])
"""

def get_reviews_for_course(db_name, course_id):

    connection = None

    try:
        connection = get_connection(db_name)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                Reviews.*,
                Users.username
            FROM Reviews
            JOIN Users
                ON Reviews.user_id = Users.user_id
            WHERE Reviews.course_id = ?
            ORDER BY Reviews.year DESC,
                     Reviews.semester,
                     Reviews.review_id DESC;
        """, (course_id,))

        reviews = cursor.fetchall()

        return reviews

    finally:
        if connection is not None:
            connection.close()



# get all the data of a user by user_id
# return None if the user does not exist
def get_user(db_name, user_id):
    """
    Return one user with the specified user ID.

    Return None if the user does not exist.
    """

    connection = None

    try:
        connection = get_connection(db_name)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM Users
            WHERE user_id = ?;
        """, (user_id,))

        user = cursor.fetchone()

        return user

    finally:
        if connection is not None:
            connection.close()


# return all the users
# sorted by user_id
def get_all_users(db_name):

    connection = None

    try:
        connection = get_connection(db_name)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM Users
            ORDER BY user_id;
        """)

        users = cursor.fetchall()

        return users

    finally:
        if connection is not None:
            connection.close()


# get the data of a user by username
# return None if the user does not exist
def get_user_by_username(db_name, username):

    connection = None

    try:
        connection = get_connection(db_name)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM Users
            WHERE username = ?;
        """, (username,))

        user = cursor.fetchone()

        return user

    finally:
        if connection is not None:
            connection.close()


# get the data of a user by email
# return None if the user does not exist
def get_user_by_email(db_name, email):

    connection = None

    try:
        connection = get_connection(db_name)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM Users
            WHERE email = ?;
        """, (email,))

        user = cursor.fetchone()

        return user

    finally:
        if connection is not None:
            connection.close()


# return all the reviews written by a user
# include course names and course codes
def get_reviews_by_user(db_name, user_id):

    connection = None

    try:
        connection = get_connection(db_name)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                Reviews.*,
                Courses.course_code,
                Courses.course_name
            FROM Reviews
            JOIN Courses
                ON Reviews.course_id = Courses.course_id
            WHERE Reviews.user_id = ?
            ORDER BY Reviews.created_at DESC,
                     Reviews.year DESC,
                     Reviews.semester,
                     Courses.course_code;
        """, (user_id,))

        reviews = cursor.fetchall()

        return reviews

    finally:
        if connection is not None:
            connection.close()

# add a course
# return course _id
def add_course(
    db_name,
    credits,
    course_name,
    course_code,
    description,
    course_type):

    connection = None

    try:
        connection = get_connection(db_name)
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO Courses
                (
                    credits,
                    course_name,
                    course_code,
                    description,
                    course_type
                )
            VALUES
                (?, ?, ?, ?, ?);
        """, (
            credits,
            course_name,
            course_code,
            description,
            course_type
        ))

        course_id = cursor.lastrowid

        connection.commit()

        return course_id

    except sqlite3.Error:
        if connection is not None:
            connection.rollback()
        raise

    finally:
        if connection is not None:
            connection.close()

# update a review
# return true if the review was successfully updated
# return false if review_id does not exist
def update_review(
    db_name,
    review_id,
    review_text,
    rating,
    difficulty,
    workload,
    year,
    semester):

    connection = None

    try:
        connection = get_connection(db_name)
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE Reviews
            SET
                review_text = ?,
                rating = ?,
                difficulty = ?,
                workload = ?,
                year = ?,
                semester = ?
            WHERE review_id = ?;
        """, (
            review_text,
            rating,
            difficulty,
            workload,
            year,
            semester,
            review_id
        ))

        review_was_updated = cursor.rowcount > 0

        connection.commit()

        return review_was_updated

    except sqlite3.Error:
        if connection is not None:
            connection.rollback()
        raise

    finally:
        if connection is not None:
            connection.close()



# increase a review's upvote by 1
# return true if the review was found
# return false if the review does not exist
def upvote_review(db_name, review_id):

    connection = None

    try:
        connection = get_connection(db_name)
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE Reviews
            SET upvotes = upvotes + 1
            WHERE review_id = ?;
        """, (review_id,))

        review_was_found = cursor.rowcount > 0

        connection.commit()

        return review_was_found

    except sqlite3.Error:
        if connection is not None:
            connection.rollback()
        raise

    finally:
        if connection is not None:
            connection.close()


# increase a reviewer's downvote by 1
# return true if the review was found
# return false if the review_id does not exist
def downvote_review(db_name, review_id):

    connection = None

    try:
        connection = get_connection(db_name)
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE Reviews
            SET downvotes = downvotes + 1
            WHERE review_id = ?;
        """, (review_id,))

        review_was_found = cursor.rowcount > 0

        connection.commit()

        return review_was_found

    except sqlite3.Error:
        if connection is not None:
            connection.rollback()
        raise

    finally:
        if connection is not None:
            connection.close()


# mark a review as flagged
# return true if the review was found
# review false if the review_id does not exist
def flag_review(db_name, review_id):

    connection = None

    try:
        connection = get_connection(db_name)
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE Reviews
            SET is_flagged = 1
            WHERE review_id = ?;
        """, (review_id,))

        review_was_found = cursor.rowcount > 0

        connection.commit()

        return review_was_found

    except sqlite3.Error:
        if connection is not None:
            connection.rollback()
        raise

    finally:
        if connection is not None:
            connection.close()

#insert review into review table
def insert_review(db_name, course_id, user_id, review_text, rating, difficulty, time, year, semester):
    
    connection = None
    
    try:
        connection = get_connection(db_name)
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO Reviews (course_id, user_id, review_text, rating, difficulty, workload, year, semester)
            VALUES(?,?,?,?,?,?,?,?)
            """,
            (course_id, user_id, review_text, rating, difficulty, time, year, semester),
        )
        connection.commit()
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed: Reviews.course_id, Reviews.user_id" in str(e):
            return "duplicate"
        return f'Error table insertion failed: {e}'
    except Exception as e:
        return f'Error table insertion failed: {e}'
    finally:
        if connection is not None:
            connection.close()
    return "review insertion successful."