###############################################################################
## This Python script provides some useful methods for interacting with the 
## SQLite database used in the CSPB Course Review Platform.
##
## CSPB 3308 Summer 2026
## Author: Team Infinity(Team 8)
##
###############################################################################

"""Database access functions for the CSPB Course Review Platform SQLite database."""

import sqlite3


def get_connection(db_name):
    """
    Create and return a database connection.

    sqlite3.Row enables you to access specific data by column name.

    Args:
        db_name: Path to the SQLite database file.

    Returns:
        An open sqlite3.Connection with row_factory set to sqlite3.Row.
    """

    connection = sqlite3.connect(db_name)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def get_all_courses(db_name):
    """
    Return a list of all courses sorted by course code.

    Args:
        db_name: Path to the SQLite database file.

    Returns:
        A list of course rows.

    Example:
        for course in courses:
            print(course["course_code"])
            print(course["course_name"])
    """

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


def get_course(db_name, course_id):
    """
    Return one course with a course ID.

    Args:
        db_name: Path to the SQLite database file.
        course_id: ID of the course to look up.

    Returns:
        The matching course row, or None if the course ID does not exist.

    Example:
        Use column names as indices to access specific data:
        course["course_name"] or course["course_code"]
    """

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


def search_courses(db_name, keyword):
    """
    Search for courses whose name or code contains the keyword.

    Args:
        db_name: Path to the SQLite database file.
        keyword: Substring to search for in course_code or course_name.

    Returns:
        A list of courses that match the search criteria.
    """

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


def get_course_averages(db_name, course_id):
    """
    Return the average rating, difficulty, and workload of a course.

    Args:
        db_name: Path to the SQLite database file.
        course_id: ID of the course to average reviews for.

    Returns:
        A row containing avg_rating, avg_difficulty, and avg_workload.
    """

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




def update_course(
    db_name,
    course_id,
    credits,
    course_name,
    course_code,
    description,
    course_type
):
    """
    Update a course.

    Args:
        db_name: Path to the SQLite database file.
        course_id: ID of the course to update.
        credits: New credit value for the course.
        course_name: New course name.
        course_code: New course code.
        description: New course description.
        course_type: New course type.

    Returns:
        True if successful, False if failed.
    """
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


def get_reviews_for_course(db_name, course_id):
    """
    Return all reviews for one course. This contains reviews themselves and the usernames of authors.

    Args:
        db_name: Path to the SQLite database file.
        course_id: ID of the course to fetch reviews for.

    Returns:
        A list of review rows.

    Example:
        for review in reviews:
            print(review["username"])
            print(review["review_text"])
    """

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



def get_user(db_name, user_id):
    """
    Get all the data of a user by user_id.

    Args:
        db_name: Path to the SQLite database file.
        user_id: ID of the user to look up.

    Returns:
        The matching user row, or None if the user does not exist.
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


def get_all_users(db_name):
    """
    Return all the users sorted by user_id.

    Args:
        db_name: Path to the SQLite database file.

    Returns:
        A list of user rows ordered by user_id.
    """

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


def get_user_by_username(db_name, username):
    """
    Get the data of a user by username.

    Args:
        db_name: Path to the SQLite database file.
        username: Username to look up.

    Returns:
        The matching user row, or None if the user does not exist.
    """

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


def get_user_by_email(db_name, email):
    """
    Get the data of a user by email.

    Args:
        db_name: Path to the SQLite database file.
        email: Email address to look up.

    Returns:
        The matching user row, or None if the user does not exist.
    """

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


def get_reviews_by_user(db_name, user_id):
    """
    Return all the reviews written by a user. Include course names and course codes.

    Args:
        db_name: Path to the SQLite database file.
        user_id: ID of the user whose reviews to fetch.

    Returns:
        A list of review rows.
    """

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


def get_recent_reviews(db_name, limit=5):
    """
    Get the 5 most recent unflagged reviews (for home page recent reviews section).

    Args:
        db_name: Path to the SQLite database file.
        limit: Maximum number of reviews to return. Defaults to 5.

    Returns:
        A list of the most recent unflagged review rows.
    """
    connection = None

    try:
        connection = get_connection(db_name)
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                Reviews.review_id,
                Reviews.course_id,
                Reviews.user_id,
                Reviews.review_text,
                Reviews.rating,
                Reviews.difficulty,
                Reviews.workload,
                Reviews.year,
                Reviews.semester,
                Reviews.created_at,
                Users.username,
                Courses.course_code,
                Courses.course_name
            FROM Reviews
            JOIN Users
                ON Reviews.user_id = Users.user_id
            JOIN Courses
                ON Reviews.course_id = Courses.course_id
            WHERE Reviews.is_flagged = 0
            ORDER BY Reviews.created_at DESC
            LIMIT ?
            """,
            (limit,)
        )

        return cursor.fetchall()

    finally:
        if connection is not None:
            connection.close()


def get_recent_reviews_for_user(db_name, user_id, limit=5):
    """
    Get the 5 most recent reviews written by a user (for recent reviews section on profile page).

    Args:
        db_name: Path to the SQLite database file.
        user_id: ID of the user whose reviews to fetch.
        limit: Maximum number of reviews to return. Defaults to 5.

    Returns:
        A list of the user's most recent review rows.
    """
    connection = None

    try:
        connection = get_connection(db_name)
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                Reviews.review_id,
                Reviews.course_id,
                Reviews.user_id,
                Reviews.review_text,
                Reviews.rating,
                Reviews.difficulty,
                Reviews.workload,
                Reviews.year,
                Reviews.semester,
                Reviews.created_at,
                Reviews.is_flagged,
                Courses.course_code,
                Courses.course_name
            FROM Reviews
            JOIN Courses
                ON Reviews.course_id = Courses.course_id
            WHERE Reviews.user_id = ?
            ORDER BY Reviews.created_at DESC
            LIMIT ?
            """,
            (user_id, limit)
        )

        return cursor.fetchall()

    finally:
        if connection is not None:
            connection.close()


def add_course(
    db_name,
    credits,
    course_name,
    course_code,
    description,
    course_type):
    """
    Add a course.

    Args:
        db_name: Path to the SQLite database file.
        credits: Number of credits for the course.
        course_name: Name of the course.
        course_code: Code of the course.
        description: Description of the course.
        course_type: Type of the course.

    Returns:
        The new course's course_id.
    """

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

def update_review(
    db_name,
    review_id,
    review_text,
    rating,
    difficulty,
    workload,
    year,
    semester):
    """
    Update a review.

    Args:
        db_name: Path to the SQLite database file.
        review_id: ID of the review to update.
        review_text: New review text.
        rating: New rating.
        difficulty: New difficulty.
        workload: New workload.
        year: New year.
        semester: New semester.

    Returns:
        True if the review was successfully updated, False if review_id does not exist.
    """

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



def upvote_review(db_name, review_id):
    """
    Increase a review's upvote by 1.

    Args:
        db_name: Path to the SQLite database file.
        review_id: ID of the review to upvote.

    Returns:
        True if the review was found, False if the review does not exist.
    """

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


def downvote_review(db_name, review_id):
    """
    Increase a reviewer's downvote by 1.

    Args:
        db_name: Path to the SQLite database file.
        review_id: ID of the review to downvote.

    Returns:
        True if the review was found, False if the review_id does not exist.
    """

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


def flag_review(db_name, review_id):
    """
    Mark a review as flagged.

    Args:
        db_name: Path to the SQLite database file.
        review_id: ID of the review to flag.

    Returns:
        True if the review was found, False if the review_id does not exist.
    """

    connection = None

    try:
        connection = get_connection(db_name)
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE Reviews
            SET is_flagged = NOT is_flagged
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

def insert_review(db_name, course_id, user_id, review_text, rating, difficulty, workload, year, semester):
    """
    Insert review into review table.

    Args:
        db_name: Path to the SQLite database file.
        course_id: ID of the course being reviewed.
        user_id: ID of the user writing the review.
        review_text: Text of the review.
        rating: Rating given by the user.
        difficulty: Difficulty given by the user.
        workload: Workload given by the user.
        year: Year the course was taken.
        semester: Semester the course was taken.

    Returns:
        "review insertion successful." on success, "duplicate" if the user has
        already reviewed this course, or an error message string on failure.
    """

    connection = None
    
    try:
        connection = get_connection(db_name)
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO Reviews (course_id, user_id, review_text, rating, difficulty, workload, year, semester)
            VALUES(?,?,?,?,?,?,?,?)
            """,
            (course_id, user_id, review_text, rating, difficulty, workload, year, semester),
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


def get_flagged_reviews(db_name):
    """
    Get all the reviews flagged by users, including the author's username, review info, and course info.

    Args:
        db_name: Path to the SQLite database file.

    Returns:
        A list of flagged review rows.
    """

    connection = None

    try:
        connection = get_connection(db_name)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                Reviews.review_id,
                Reviews.review_text,
                Reviews.rating,
                Reviews.difficulty,
                Reviews.workload,
                Reviews.year,
                Reviews.semester,
                Reviews.created_at,
                Reviews.upvotes,
                Reviews.course_id,
                Reviews.downvotes,
                Users.username,
                Courses.course_code,
                Courses.course_name
            FROM Reviews
            JOIN Users
                ON Reviews.user_id = Users.user_id
            JOIN Courses
                ON Reviews.course_id = Courses.course_id
            WHERE Reviews.is_flagged = 1
            ORDER BY Reviews.created_at DESC;
        """)

        flagged_reviews = cursor.fetchall()

        return flagged_reviews

    finally:
        if connection is not None:
            connection.close()


def get_review(db_name, review_id):
    """
    Get a specific review by review_id. This also returns course name and course code.

    Args:
        db_name: Path to the SQLite database file.
        review_id: ID of the review to look up.

    Returns:
        The matching review row, or None if the review does not exist.
    """

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
                Reviews.created_at,
                Courses.course_code,
                Courses.course_name
            FROM Reviews
            JOIN Courses
                ON Reviews.course_id = Courses.course_id
            WHERE Reviews.review_id = ?;
        """, (review_id,))

        review = cursor.fetchone()

        return review

    finally:
        if connection is not None:
            connection.close()


def get_review_by_user_and_course(db_name, user_id, course_id):
    """
    Return a user's review for a course.

    Args:
        db_name: Path to the SQLite database file.
        user_id: ID of the user.
        course_id: ID of the course.

    Returns:
        The matching review row, or None if the user has not reviewed this course.
    """

    connection = None

    try:
        connection = get_connection(db_name)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM Reviews
            WHERE user_id = ?
              AND course_id = ?;
        """, (
            user_id,
            course_id
        ))

        return cursor.fetchone()

    finally:
        if connection is not None:
            connection.close()

