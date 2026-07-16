## Project Milestone 5: SQL Design
**Team:** Team 8 - Infinity
**Project:** CSPB Course Reviews  
**Purpose:** Database design and testing specification for developers

---

## Overview

This document describes the **database schema**, **table relationships**, and **data access methods** for the CSPB Course Reviews application. It is intended as a **developer-facing design document** that clearly defines how data is stored, accessed, and validated.

This document answers the following questions:
- What tables exist in the database?
- What fields and constraints do those tables contain?
- How are tables related?
- What data access methods are required?
- Which pages depend on which data?
- How do we test both the schema and the access routines?

The backend uses **SQLite** and **Python**

---

# Database Tables

At minimum, the system requires the following tables:
- `Users`
- `Courses`
- `Reviews`


Each table is described below.

---

## 1) Table: Users

### Table Description
Stores user account information.

### Fields
### Users Table Schema

| Field name | Description | Constraints |
| :--- | :--- | :--- |
| **User ID** | Unique identifier for each user | Primary key, `int` |
| **Username** | The account name of the user | `string` |
| **Admin** | Indicates whether the user has administrator privileges | `bool` |
| **Email** | The user's email address | `string` |
| **Password Hash** | Secure cryptographic hash of the user's password | |


### Relationships
- One-to-many with `Reviews`
- Many-to-many with `Courses`


### Table Tests

**Use Case Name:** Create a user  
**Description:** Verify user creation 
**Pre-conditions:** Database running  
**Test Steps:**
1. Insert a valid user row
2. Query by email  
**Expected Result:** User row exists  
**Actual Result:** User returned by query  
**Status:** Pass  
**Post-conditions:** User persisted  

---

## 2) Table: Courses

### Table Description
Stores CSPB course information

### Fields
### Courses Table Schema

| Field name | Description | Constraints |
| :--- | :--- | :--- |
| **Course ID** | Unique identifier for each course | Primary key, `int` |
| **Semester** | The academic semester in which the course is offered | `string` |
| **Year** | The calendar year the course takes place | `int` |
| **Credits** | The academic credit value of the course | `int` |
| **Course Name/Code** | The official name or code representing the course | `string` |
| **Description** | A brief summary of the course content and syllabus | `string` |
| **Core** | Indicates whether the course is a core requirement | `bool` |


### Relationships
- Many-to-many with `Users`
- One-to-many with `Reviews


### Table Tests

**Use Case Name:** Create a course 
**Description:** Verify course creation  
**Pre-conditions:** database running  
**Test Steps:**
1. Insert a valid course row
2. Query by course name
**Expected Result:** course row created  
**Actual Result:** course returned  
**Status:** Pass
**Post-conditions:** Course persisted    

---

## 3) Table: Reviews

### Table Description
Stores reviews for each course

### Fields
### Reviews Table Schema

| Field name | Description | Constraints |
| :--- | :--- | :--- |
| **Review ID** | Unique identifier for each review | Primary key, `int` |
| **Course ID** | The ID of the course being reviewed | Foreign key (references `Courses.Course ID`), `int` |
| **User ID** | The ID of the user who wrote the review | Foreign key (references `Users.User ID`), `int` |
| **Review** | The text content of the review | `string` |
| **Upvotes** | The number of positive votes the review has received | `int` |
| **Downvotes** | The number of negative votes the review has received | `int` |
| **Flagged** | Indicates whether the review has been reported or flagged | `bool` |
| **Rating** | The numerical course rating given by the user | `dbl` |
| **Difficulty** | The perceived difficulty level of the course | `dbl` |
| **Time** | The estimated hours per week spent on the course | `dbl` |


### Relationships
- Many-to-one with `Courses`
- Many-to-one with `Users`

### Table Tests

**Use Case Name:** Add a review on a course  
**Description:** Verify review creation  
**Test Steps:**
1. Insert a valid review row
2. Query by user name and course name  
**Expected Result:** Review exists
**Actual Result:** Review returned  
**Status:** Pass  
**Post-conditions:** Review persisted  
---



# Data Access Methods

Each table has at least one access method.

---

## Access Method: is_admin

### Description
Returns boolean from value from the Users table value that indicates the user is or is not an admin.

### Parameters
- user_id (int)

### Return Values
- True or False

### Tests
1. Call method and receive valid return for user_id  
2. Call method with invalid user_id and receive appropriate error

—

## Access Method: get_username_by_userid

### Description
Fetches the username of a user by user_id
This is used whenever the platform needs to greet a user or display the author of a review

### Parameters
- user_id (integer)

### Return Values
- Username or null

### Tests

**Use Case Name:** Retrieve username of a user  
**Pre-conditions:** User exists  
**Test Steps:**
1. Call method with known user_id 
**Expected Result:** Username returned  
**Post-conditions:** None 


## Access Method: get_course_reviews

### Description
Returns all reviews for a given course from the reviews table

### Parameters
- course_id (int)

### Return Values
- list of review objects.

### Tests

1. A function call returns a complete list of review objects.
2. A function call returns an empty list if there are no reviews for the course.

—

## Access Method: get_average_course_rating

### Description
Fetches the average rating of a course

### Parameters
- course_id (integer)

### Return Values
- Course rating (REAL) or NULL (no rating available)

### Tests

**Use Case Name:** Retrieve the average rating of a course 
**Pre-conditions:** Course exists  
**Test Steps:**
1. Call method with known course_id
2. Retrieve all individual ratings
3. Use AVG(rating) to calculate the average  
**Expected Result:** Course rating average returned  
**Post-conditions:** None 


## Access Method: get_courses

### Description 
Returns a list of course objects from the Courses table.

### Parameters
-none

### Return Values
-list of all the courses (as objects) in the database

### Tests
1. Function returns a complete list of Course objects

—

## Access Method: get_course_id_by_keyword

### Description
Fetches a list of courses that contain a keyword

### Parameters
- keyword (string)

### Return Values
- None or one or multiple rows of courses returned  

### Tests

**Use Case Name:** Search courses by keywords  
**Pre-conditions:** Database running  
**Test Steps:**
1. Call method with keywords
2. Use SQL command Like to match the keyword   
**Expected Result:** None or one or multiple rows of courses returned  
**Post-conditions:** None 



## Notes
- Constraints enforced at DB and ORM levels
- All access methods wrapped in service layer
- Tests executable via integration test suite
