# CSPB 3308 Team Project
# CSPB Coruse Review Platform

# This Python script creates the Users, Courses, and Reviews table
# It also inserts initial test data

import sqlite3

DATABASE_NAME = "course_reviews.db"

# Create the Users, Courses, and Reviews tables
# db_name: the name of the SQLite database file
def create_table(db_name):

    connection = None

    try:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        # enable foreign keys
        cursor.execute("PRAGMA foreign_keys = ON")

        # Users table
        # enforce some initial value checks
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                user_id INTEGER PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                is_admin INTEGER NOT NULL DEFAULT 0
                    CHECK (is_admin IN (0, 1)),
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            )
        """)

        # Courses table
        # enforce some initial value checks
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Courses (
                course_id INTEGER PRIMARY KEY,
                course_name TEXT NOT NULL,
                course_code TEXT NOT NULL UNIQUE,
                credits INTEGER NOT NULL
                    CHECK (credits > 0),
                description TEXT,
                course_type TEXT NOT NULL
                    CHECK (course_type IN ('Core', 'Elective'))
            )
        """)

        # Reviews table
        # enforce some initial value checks
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Reviews (
                review_id INTEGER PRIMARY KEY,
                course_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                review_text TEXT,
                upvotes INTEGER DEFAULT 0
                    CHECK (upvotes >= 0),
                downvotes INTEGER DEFAULT 0
                    CHECK (downvotes >= 0),
                is_flagged INTEGER DEFAULT 0
                    CHECK (is_flagged IN (0, 1)),
                rating INTEGER NOT NULL
                    CHECK (rating BETWEEN 1 AND 5),
                difficulty INTEGER NOT NULL
                    CHECK (difficulty BETWEEN 1 AND 5),
                workload INTEGER NOT NULL
                    CHECK (workload >= 0),
                year INTEGER NOT NULL,
                semester TEXT NOT NULL
                    CHECK (semester IN ('Spring', 'Summer', 'Fall')),

                FOREIGN KEY (course_id)
                    REFERENCES Courses(course_id),

                FOREIGN KEY (user_id)
                    REFERENCES Users(user_id),

                UNIQUE (course_id, user_id)
            )
        """)

        connection.commit()

    # error handling
    except sqlite3.Error as error:
        if connection is not None:
            connection.rollback()

        print("Database error:", error)
        raise

    # always close the DB connection 
    finally:
        if connection is not None:
            connection.close()


# insert initial test data into the database
# db_name: the name of the SQLite database file
def insert_test_data(db_name):

    connection = None

    try:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        # enalbe foreign keys
        cursor.execute("PRAGMA foreign_keys = ON")

 
        # test data for the Users table

        cursor.execute("""
            INSERT INTO Users
                (username, is_admin, email, password_hash)
            VALUES
                ('Algorithm_Puppy', 1,
                 'Algorithm_Puppy@colorado.edu',
                 'ABCD1234');
        """)

        cursor.execute("""
            INSERT INTO Users
                (username, is_admin, email, password_hash)
            VALUES
                ('ML_Dolphin', 0,
                 'ML_Dolphin@colorado.edu',
                 'EFGH5678');
        """)

        cursor.execute("""
            INSERT INTO Users
                (username, is_admin, email, password_hash)
            VALUES
                ('Programming_Kitten', 1,
                 'Programming_Kitten@colorado.edu',
                 'DCBA4321');
        """)

        cursor.execute("""
            INSERT INTO Users
                (username, is_admin, email, password_hash)
            VALUES
                ('SoftwareDev_Rabbit', 0,
                 'SoftwareDev_Rabbit@colorado.edu',
                 'HGFE8765');
        """)

        # test data for the Courses table
 
        cursor.execute("""
            INSERT INTO Courses
                (credits, course_name, course_code,
                 description, course_type)
            VALUES
                (4,
                 'Computer Science 1: Starting Computing',
                 'CSPB 1300',
                 'The course covers techniques for writing computer programs in high-level programming languages to solve problems of interest in a range of application domains.',
                 'Core');
        """)

        cursor.execute("""
            INSERT INTO Courses
                (credits, course_name, course_code,
                 description, course_type)
            VALUES
                (4,
                 'Computer Science 2: Data Structures',
                 'CSPB 2270',
                 'Studies data abstractions (e.g., stacks, queues, lists, trees) and their representation techniques (e.g., linking, arrays). Introduces concepts used in algorithm design and analysis including criteria for selecting data structures to fit their applications.',
                 'Core');
        """)

        cursor.execute("""
            INSERT INTO Courses
                (credits, course_name, course_code,
                 description, course_type)
            VALUES
                (3,
                 'Discrete Structures',
                 'CSPB 2824',
                 'The course covers fundamental ideas from discrete mathematics, especially for computer science students. It focuses on topics that will be foundational for future courses.',
                 'Core');
        """)

        cursor.execute("""
            INSERT INTO Courses
                (credits, course_name, course_code,
                 description, course_type)
            VALUES
                (3,
                 'Linear Algebra with Computer Science Applications',
                 'CSPB 2820',
                 'Introduces the fundamentals of linear algebra in the context of computer science applications. Includes vector spaces, matrices, linear systems and eigenvalues. Includes the basics of floating point computation and numerical linear algebra.',
                 'Elective');
        """)

        # test data for the Reviews table

        cursor.execute("""
            INSERT INTO Reviews
                (course_id, user_id, review_text,
                 upvotes, downvotes, is_flagged,
                 rating, difficulty, workload,
                 year, semester)
            VALUES
                (1, 1,
                 'The course is great if you are new to coding. Too easy for advanced students.',
                 3, 1, 0,
                 4, 3, 4,
                 2024, 'Spring');
        """)

        cursor.execute("""
            INSERT INTO Reviews
                (course_id, user_id, review_text,
                 upvotes, downvotes, is_flagged,
                 rating, difficulty, workload,
                 year, semester)
            VALUES
                (1, 2,
                 'A good intro course. It taught me how to code.',
                 5, 0, 0,
                 5, 3, 6,
                 2025, 'Summer');
        """)

        cursor.execute("""
            INSERT INTO Reviews
                (course_id, user_id, review_text,
                 upvotes, downvotes, is_flagged,
                 rating, difficulty, workload,
                 year, semester)
            VALUES
                (2, 3,
                 'A challenging course. Some assignments can take a lot of time.',
                 3, 0, 0,
                 4, 5, 10,
                 2024, 'Fall');
        """)

        cursor.execute("""
            INSERT INTO Reviews
                (course_id, user_id, review_text,
                 upvotes, downvotes, is_flagged,
                 rating, difficulty, workload,
                 year, semester)
            VALUES
                (2, 4,
                 'A solid intro to important data structures.',
                 4, 2, 0,
                 5, 4, 8,
                 2024, 'Spring');
        """)

        cursor.execute("""
            INSERT INTO Reviews
                (course_id, user_id, review_text,
                 upvotes, downvotes, is_flagged,
                 rating, difficulty, workload,
                 year, semester)
            VALUES
                (3, 1,
                 'I have no idea why we must study math. I just want to learn how to code.',
                 1, 4, 1,
                 1, 5, 12,
                 2025, 'Summer');
        """)

        cursor.execute("""
            INSERT INTO Reviews
                (course_id, user_id, review_text,
                 upvotes, downvotes, is_flagged,
                 rating, difficulty, workload,
                 year, semester)
            VALUES
                (3, 2,
                 'A good foundation course. You will need discrete math for the algorithms class.',
                 3, 2, 0,
                 4, 3, 8,
                 2024, 'Fall');
        """)

        cursor.execute("""
            INSERT INTO Reviews
                (course_id, user_id, review_text,
                 upvotes, downvotes, is_flagged,
                 rating, difficulty, workload,
                 year, semester)
            VALUES
                (4, 3,
                 'Make sure to take this class if you want to study machine learning.',
                 4, 0, 0,
                 4, 3, 6,
                 2025, 'Fall');
        """)

        cursor.execute("""
            INSERT INTO Reviews
                (course_id, user_id, review_text,
                 upvotes, downvotes, is_flagged,
                 rating, difficulty, workload,
                 year, semester)
            VALUES
                (4, 4,
                 'Boring class!',
                 0, 3, 1,
                 1, 4, 8,
                 2026, 'Spring');
        """)

        connection.commit()

    # error handling
    except sqlite3.Error:
        if connection is not None:
            connection.rollback()
        raise

    # always close the connection
    finally:
        if connection is not None:
            connection.close()


def main():
    create_table(DATABASE_NAME)
    insert_test_data(DATABASE_NAME)
    print("Database created successfully.")

if __name__ == "__main__":
    main()