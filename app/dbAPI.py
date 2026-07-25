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
                Reviews.review_id,
                Reviews.course_id,
                Reviews.user_id,
                Reviews.review_text,
                Reviews.upvotes,
                Reviews.downvotes,
                Reviews.is_flagged,
                Reviews.rating,
                Reviews.difficulty,
                Reviews.workload,
                Reviews.year,
                Reviews.semester,
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
