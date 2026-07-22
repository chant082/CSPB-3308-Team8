import sqlite3
from config import DATABASE


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  
    return conn

def init_db():
    conn = get_db()
    with open("schema.sql") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

#get a single course by id
def get_course(course_id):
    conn = get_db()
    course = conn.execute(
        "SELECT * FROM Courses WHERE course_id = ?", (course_id,)
    ).fetchone()
    conn.close()
    return course

#insert review into review table
def insert_review(course_id, user_id, review, rating, difficulty, time):
    conn = get_db()
    conn.execute(
        """
        INSERT INTO Reviews (course_id, user_id, review, rating, difficulty, time)
        VALUES(?,?,?,?,?,?)
        """,
        (course_id, user_id, review, rating, difficulty, time),
    )
    conn.commit()
    conn.close()



