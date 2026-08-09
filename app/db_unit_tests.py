###############################################################################
## This Python script performs unit tests for database API functions
## This uses Python's unittest framework
## CSPB 3308 Summer 2026
## Author: Team Infinity(Team 8)
##
###############################################################################

import os
import sqlite3
import unittest

import create_db
import dbAPI


DB_NAME = "unit_test.db"

# Create a fresh unit_test.db before every test so that tests do not affect one another.
class TestDBAPI(unittest.TestCase):

    def setUp(self):
        if os.path.exists(DB_NAME):
            os.remove(DB_NAME)

        create_db.create_table(DB_NAME)
        self.insert_mock_data()

    # Always remove unit_test.db after each test.
    def tearDown(self):
        if os.path.exists(DB_NAME):
            os.remove(DB_NAME)

    # Insert mock data 
    def insert_mock_data(self):

        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()

        cursor.execute("PRAGMA foreign_keys = ON")

        # Users table
        cursor.execute("""
            INSERT INTO Users
                (username, is_admin, email, password_hash)
            VALUES
                ('Graph_Lion', 1,
                 'Graph_Lion@colorado.edu',
                 'TEST1111');
        """)

        cursor.execute("""
            INSERT INTO Users
                (username, is_admin, email, password_hash)
            VALUES
                ('Cloud_Otter', 0,
                 'Cloud_Otter@colorado.edu',
                 'TEST2222');
        """)

        cursor.execute("""
            INSERT INTO Users
                (username, is_admin, email, password_hash)
            VALUES
                ('Security_Fox', 0,
                 'Security_Fox@colorado.edu',
                 'TEST3333');
        """)

        # Courses table
        cursor.execute("""
            INSERT INTO Courses
                (credits, course_name, course_code,
                 description, course_type)
            VALUES
                (4,
                 'Foundations of Programming',
                 'CSPB 1111',
                 'An introductory programming course used for unit testing.',
                 'Core');
        """)

        cursor.execute("""
            INSERT INTO Courses
                (credits, course_name, course_code,
                 description, course_type)
            VALUES
                (4,
                 'Algorithms and Data Structures',
                 'CSPB 2222',
                 'A course about Algorithms and Data Structures.',
                 'Core');
        """)

        cursor.execute("""
            INSERT INTO Courses
                (credits, course_name, course_code,
                 description, course_type)
            VALUES
                (3,
                 'Introduction to Data Science',
                 'CSPB 3333',
                 'An elective introduction to data analysis.',
                 'Elective');
        """)

        cursor.execute("""
            INSERT INTO Courses
                (credits, course_name, course_code,
                 description, course_type)
            VALUES
                (3,
                 'Web Applications',
                 'CSPB 4444',
                 'A web development course with no reviews initially.',
                 'Elective');
        """)

        # Reviews table
        cursor.execute("""
            INSERT INTO Reviews
                (course_id, user_id, review_text,
                 upvotes, downvotes, is_flagged,
                 rating, difficulty, workload,
                 year, semester, created_at)
            VALUES
                (1, 1,
                 'A clear introduction to programming concepts.',
                 2, 0, 0,
                 4, 3, 6,
                 2025, 'Fall',
                 '2025-10-10 10:00:00');
        """)

        cursor.execute("""
            INSERT INTO Reviews
                (course_id, user_id, review_text,
                 upvotes, downvotes, is_flagged,
                 rating, difficulty, workload,
                 year, semester, created_at)
            VALUES
                (1, 2,
                 'Useful course, but some assignments were challenging.',
                 1, 2, 1,
                 5, 4, 8,
                 2026, 'Spring',
                 '2026-03-10 12:30:00');
        """)

        cursor.execute("""
            INSERT INTO Reviews
                (course_id, user_id, review_text,
                 upvotes, downvotes, is_flagged,
                 rating, difficulty, workload,
                 year, semester, created_at)
            VALUES
                (2, 1,
                 'The algorithms were interesting but demanding.',
                 3, 1, 0,
                 3, 5, 12,
                 2025, 'Summer',
                 '2025-08-01 09:15:00');
        """)

        cursor.execute("""
            INSERT INTO Reviews
                (course_id, user_id, review_text,
                 upvotes, downvotes, is_flagged,
                 rating, difficulty, workload,
                 year, semester, created_at)
            VALUES
                (3, 3,
                 'A practical and approachable data science elective.',
                 4, 0, 0,
                 5, 2, 4,
                 2026, 'Spring',
                 '2026-04-20 14:45:00');
        """)

        connection.commit()
        connection.close()

 
    # Connection

    def test_get_connection(self):
        connection = dbAPI.get_connection(DB_NAME)

        self.assertEqual(connection.row_factory, sqlite3.Row)

        foreign_keys = connection.execute("PRAGMA foreign_keys").fetchone()[0]
        self.assertEqual(foreign_keys, 1)

        connection.close()


    # Course APIs

    def test_get_all_courses(self):
        courses = dbAPI.get_all_courses(DB_NAME)

        actual = [
            (course["course_code"], course["course_name"])
            for course in courses
        ]

        expected = [
            ("CSPB 1111", "Foundations of Programming"),
            ("CSPB 2222", "Algorithms and Data Structures"),
            ("CSPB 3333", "Introduction to Data Science"),
            ("CSPB 4444", "Web Applications"),
        ]

        self.assertEqual(actual, expected)

    def test_get_course(self):
        course = dbAPI.get_course(DB_NAME, 2)

        expected = {
            "course_id": 2,
            "course_name": "Algorithms and Data Structures",
            "course_code": "CSPB 2222",
            "credits": 4,
            "description": "A course about Algorithms and Data Structures.",
            "course_type": "Core",
        }

        actual = dict(course)

        self.assertEqual(actual, expected)

    def test_search_courses(self):
        courses = dbAPI.search_courses(DB_NAME, "Data Science")

        actual = [
            (course["course_code"], course["course_name"])
            for course in courses
        ]

        expected = [
            ("CSPB 3333", "Introduction to Data Science")
        ]

        self.assertEqual(actual, expected)

    def test_get_course_averages(self):
        averages = dbAPI.get_course_averages(DB_NAME, 1)

        expected = (4.5, 3.5, 7.0)

        actual = (
            averages["avg_rating"],
            averages["avg_difficulty"],
            averages["avg_workload"],
        )

        self.assertEqual(actual, expected)

    def test_get_course_averages_no_reviews(self):
        averages = dbAPI.get_course_averages(DB_NAME, 4)

        expected = (0, 0, 0)

        actual = (
            averages["avg_rating"],
            averages["avg_difficulty"],
            averages["avg_workload"],
        )

        self.assertEqual(actual, expected)

    def test_update_course(self):
        result = dbAPI.update_course(
            DB_NAME,
            2,
            3,
            "Advanced Algorithms",
            "CSPB 2250",
            "Updated course description.",
            "Elective",
        )

        course = dbAPI.get_course(DB_NAME, 2)

        expected = (
            True,
            3,
            "Advanced Algorithms",
            "CSPB 2250",
            "Updated course description.",
            "Elective",
        )

        actual = (
            result,
            course["credits"],
            course["course_name"],
            course["course_code"],
            course["description"],
            course["course_type"],
        )

        self.assertEqual(actual, expected)

    def test_add_course(self):
        course_id = dbAPI.add_course(
            DB_NAME,
            3,
            "Computer Networks",
            "CSPB 5555",
            "An introductory networking course.",
            "Elective",
        )

        course = dbAPI.get_course(DB_NAME, course_id)

        expected = (
            5,
            "Computer Networks",
            "CSPB 5555",
            3,
            "An introductory networking course.",
            "Elective",
        )

        actual = (
            course["course_id"],
            course["course_name"],
            course["course_code"],
            course["credits"],
            course["description"],
            course["course_type"],
        )

        self.assertEqual(actual, expected)


    # User APIs

    def test_get_user(self):
        user = dbAPI.get_user(DB_NAME, 2)

        expected = (
            2,
            "Cloud_Otter",
            0,
            "Cloud_Otter@colorado.edu",
            "TEST2222",
        )

        actual = (
            user["user_id"],
            user["username"],
            user["is_admin"],
            user["email"],
            user["password_hash"],
        )

        self.assertEqual(actual, expected)

    def test_get_all_users(self):
        users = dbAPI.get_all_users(DB_NAME)

        actual = [
            (user["username"], user["email"], user["is_admin"])
            for user in users
        ]

        expected = [
            ("Graph_Lion", "Graph_Lion@colorado.edu", 1),
            ("Cloud_Otter", "Cloud_Otter@colorado.edu", 0),
            ("Security_Fox", "Security_Fox@colorado.edu", 0),
        ]

        self.assertEqual(actual, expected)

    def test_get_user_by_username(self):
        user = dbAPI.get_user_by_username(DB_NAME, "Security_Fox")

        expected = (
            3,
            "Security_Fox",
            "Security_Fox@colorado.edu",
        )

        actual = (
            user["user_id"],
            user["username"],
            user["email"],
        )

        self.assertEqual(actual, expected)

    def test_get_user_by_email(self):
        user = dbAPI.get_user_by_email(
            DB_NAME,
            "Graph_Lion@colorado.edu"
        )

        expected = (
            1,
            "Graph_Lion",
            1,
        )

        actual = (
            user["user_id"],
            user["username"],
            user["is_admin"],
        )

        self.assertEqual(actual, expected)

 
    # review retrieval APIs

    def test_get_reviews_for_course(self):
        reviews = dbAPI.get_reviews_for_course(DB_NAME, 1)

        # This course has two reviews. The most recent review should appear first.
        first_review = reviews[0]

        expected = (
            2,
            "Cloud_Otter",
            5,
            "Useful course, but some assignments were challenging.",
        )

        actual = (
            first_review["review_id"],
            first_review["username"],
            first_review["rating"],
            first_review["review_text"],
        )

        self.assertEqual(actual, expected)

    def test_get_reviews_by_user(self):
        reviews = dbAPI.get_reviews_by_user(DB_NAME, 1)

        # This user has two reviews. The most recent review should appear first.
        first_review = reviews[0]

        expected = (
            1,
            "CSPB 1111",
            "Foundations of Programming",
            "A clear introduction to programming concepts.",
        )

        actual = (
            first_review["review_id"],
            first_review["course_code"],
            first_review["course_name"],
            first_review["review_text"],
        )

        self.assertEqual(actual, expected)

    def test_get_recent_reviews(self):
        reviews = dbAPI.get_recent_reviews(DB_NAME, limit=2)

        # Review 2 is newer but flagged, so it must not be returned.
        actual = [review["review_id"] for review in reviews]

        expected = [4, 1]

        self.assertEqual(actual, expected)

    def test_get_recent_reviews_for_user(self):
        reviews = dbAPI.get_recent_reviews_for_user(
            DB_NAME,
            user_id=1,
            limit=1
        )

        actual = (
            len(reviews),
            reviews[0]["review_id"],
            reviews[0]["course_code"],
        )

        expected = (
            1,
            1,
            "CSPB 1111",
        )

        self.assertEqual(actual, expected)

    def test_get_flagged_reviews(self):
        reviews = dbAPI.get_flagged_reviews(DB_NAME)

        self.assertEqual(len(reviews), 1)

        review = reviews[0]

        expected = (
            2,
            "Cloud_Otter",
            "CSPB 1111",
            "Foundations of Programming",
            "Useful course, but some assignments were challenging.",
        )

        actual = (
            review["review_id"],
            review["username"],
            review["course_code"],
            review["course_name"],
            review["review_text"],
        )

        self.assertEqual(actual, expected)

    def test_get_review(self):
        review = dbAPI.get_review(DB_NAME, 3)

        expected = (
            3,
            2,
            1,
            "CSPB 2222",
            "Algorithms and Data Structures",
            3,
            5,
            12,
        )

        actual = (
            review["review_id"],
            review["course_id"],
            review["user_id"],
            review["course_code"],
            review["course_name"],
            review["rating"],
            review["difficulty"],
            review["workload"],
        )

        self.assertEqual(actual, expected)

    def test_get_review_by_user_and_course(self):
        review = dbAPI.get_review_by_user_and_course(
            DB_NAME,
            user_id=3,
            course_id=3
        )

        expected = (
            4,
            "A practical and approachable data science elective.",
            5,
        )

        actual = (
            review["review_id"],
            review["review_text"],
            review["rating"],
        )

        self.assertEqual(actual, expected)


    # Review modification APIs

    def test_update_review(self):
        result = dbAPI.update_review(
            DB_NAME,
            1,
            "Updated unit-test review text.",
            5,
            2,
            5,
            2026,
            "Spring",
        )

        review = dbAPI.get_review(DB_NAME, 1)

        expected = (
            True,
            "Updated unit-test review text.",
            5,
            2,
            5,
            2026,
            "Spring",
        )

        actual = (
            result,
            review["review_text"],
            review["rating"],
            review["difficulty"],
            review["workload"],
            review["year"],
            review["semester"],
        )

        self.assertEqual(actual, expected)

    def test_upvote_review(self):
        result = dbAPI.upvote_review(DB_NAME, 1)
        review = dbAPI.get_review(DB_NAME, 1)

        expected = (True, 3)
        actual = (result, review["upvotes"])

        self.assertEqual(actual, expected)

    def test_downvote_review(self):
        result = dbAPI.downvote_review(DB_NAME, 1)
        review = dbAPI.get_review(DB_NAME, 1)

        expected = (True, 1)
        actual = (result, review["downvotes"])

        self.assertEqual(actual, expected)

    def test_flag_review(self):
        result = dbAPI.flag_review(DB_NAME, 1)
        review = dbAPI.get_review(DB_NAME, 1)

        # Review 1 begins unflagged (0)
        # flag_review() should toggle it to 1.
        expected = (True, 1)
        actual = (result, review["is_flagged"])

        self.assertEqual(actual, expected)

    def test_insert_review(self):
        result = dbAPI.insert_review(
            DB_NAME,
            course_id=4,
            user_id=3,
            review_text="A new review inserted by the unit test.",
            rating=4,
            difficulty=3,
            workload=7,
            year=2026,
            semester="Summer",
        )

        review = dbAPI.get_review_by_user_and_course(
            DB_NAME,
            user_id=3,
            course_id=4
        )

        expected = (
            "review insertion successful.",
            "A new review inserted by the unit test.",
            4,
            3,
            7,
            2026,
            "Summer",
        )

        actual = (
            result,
            review["review_text"],
            review["rating"],
            review["difficulty"],
            review["workload"],
            review["year"],
            review["semester"],
        )

        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
