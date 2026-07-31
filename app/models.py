import sqlite3
from config import DATABASE
#CURRENTLY UNUSED BUT SAVED FOR FUTURE IMPLEMENTATION:
#the Review object that we can customize 
class Review:
    def __init__(self, review_id: int, course_id: int, user_id: int, review_text: str,
                 upvotes: int, downvotes: int, is_flagged: bool, rating: int,
                 difficulty: int, workload: int, year: int, semester: str):
        self.__review_id = review_id
        self.__course_id = course_id
        self.__user_id = user_id
        self.__review_text = review_text
        self.__upvotes = upvotes
        self.__downvotes = downvotes
        self.__is_flagged = is_flagged
        self.__rating = rating
        self.__difficulty = difficulty
        self.__workload = workload
        self.__year = year
        self.__semester = semester

    def get_review_id(self) -> int:
        return self.__review_id

    def get_course_id(self) -> int:
        return self.__course_id

    def get_user_id(self) -> int:
        return self.__user_id

    def get_review_text(self) -> str:
        return self.__review_text

    def get_upvotes(self) -> int:
        return self.__upvotes

    def get_downvotes(self) -> int:
        return self.__downvotes

    def get_is_flagged(self) -> bool:
        return self.__is_flagged

    def get_rating(self) -> int:
        return self.__rating

    def get_difficulty(self) -> int:
        return self.__difficulty

    def get_workload(self) -> int:
        return self.__workload

    def get_year(self) -> int:
        return self.__year

    def get_semester(self) -> str:
        return self.__semester


class Course:
    def __init__(self, course_id: int, course_name: str, description: str,
                 credits: int, isCore: bool, reviews: list[Review]):
        self.__course_id = course_id
        self.__course_name = course_name
        self.__description = description
        self.__credits = credits
        self.__is_core = isCore
        self.__reviews = reviews

    def get_course_id(self) -> int:
        return self.__course_id

    def get_course_name(self) -> str:
        return self.__course_name

    def get_course_description(self) -> str:
        return self.__description

    def get_cretdits(self) -> int:
        return self.__credits

    def get_isCore(self) -> bool:
        return self.__is_core

    def get_reviews(self) -> list[Review]:
        return self.__reviews

    def get_average_rating(self) -> float:
        if not self.__reviews:
            return 0.0
        return sum(review.get_rating() for review in self.__reviews) / len(self.__reviews)

    def get_average_difficulty(self) -> float:
        if not self.__reviews:
            return 0.0
        return sum(review.get_difficulty() for review in self.__reviews) / len(self.__reviews)

    def get_average_workload(self) -> float:
        if not self.__reviews:
            return 0.0
        return sum(review.get_workload() for review in self.__reviews) / len(self.__reviews)

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

#get a course and its reviews as Course/Review objects
def get_course_object(course_id):
    conn = get_db()
    course_row = conn.execute(
        "SELECT * FROM Courses WHERE course_id = ?", (course_id,)
    ).fetchone()
    if course_row is None:
        conn.close()
        return None

    review_rows = conn.execute(
        "SELECT * FROM Reviews WHERE course_id = ?", (course_id,)
    ).fetchall()
    conn.close()

    reviews = [
        Review(
            row["review_id"], row["course_id"], row["user_id"], row["review_text"],
            row["upvotes"], row["downvotes"], bool(row["is_flagged"]), row["rating"],
            row["difficulty"], row["workload"], row["year"], row["semester"],
        )
        for row in review_rows
    ]

    return Course(
        course_row["course_id"], course_row["course_name"], course_row["description"],
        course_row["credits"], course_row["course_type"] == "Core", reviews,
    )