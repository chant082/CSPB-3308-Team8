# CSPB Course Reviews Final Report

## Milestone 8: Final Report Submission

## Project Title
CSPB Course Reviews

## Team Members
- Hannah Pfeifer
- Adam Chathankeo
- Sean Lin
- Craig Sanders

## Required Links

- Google Doc (Main document used for project tracking and planning): https://docs.google.com/document/d/1nF79oh0ICRbWhd5ra6tRL8jqTmVE5mIKCr6LFDHrqlA/edit?usp=sharing
- Version control repository (GitHub): https://github.com/chant082/CSPB-3308-Team8
- Project tracker (no longer used): https://trello.com/w/userworkspace23812499

## Repository Readiness
All team members have verified that their latest work is pushed to the remote
repository.
The repository contains the following required files and assets:
- README.md
- WEEKLY_STATUS.md
- PAGE_TESTING.md
- SQL_TESTING.md
- FINAL_REPORT.md
- Project presentation files from the Presentation Milestone	
- Video of demo
- Source code (frontend and backend)
- Test cases (unit and integration)
- Source documentation and auto-generated documentation files

## Final Status Report
![Logo](app/static/images/CSPB_horiz_logo.png)
During the semester-long project in CSPB 3308: Software Development Methods and Tools, Team Infinity (Team 8) set out to create a web-based system for students enrolled in the University of Colorado Boulder Post-Baccalaureate in Computer Science program. The goal of the project was to provide students with a centralized platform for communicating and sharing information about courses within the program. Through this system, students can view course information, share their experiences through course reviews, and gain insight from other students when making decisions about their coursework.

### What We Completed
Working MVP that delivers essential features which were tested and functions including:
Flask user session and authentication
Flouse routes, CSS, and HTML for individual pages (Login, Sign Up, Logout, about, etc.)
SQL Database structure and methods (dbAPI, create and reset database)
Ability for Local deployment of application
Account Creation and Edit Profile
![Profile](app/static/images/profile.png)

Login / Logout
![Home Page](app/static/images/homepage.png)

Browse Courses, Look at Course Statistics, and Read reviews
![Browse Courses](app/static/images/course_list.png)

Write one review per course (For User / Admin)
![Review](app/static/images/write_review.png)

Edit reviews (If written by that User / Admin)

Upvote / Downvote / Flag reviews (For User / Admin)
![Course Review](app/static/images/course_management.png)

Admin Panel (Admin only) allowing to create / edit courses, view other uses roles, and moderate flagged reviews
![Course Management](app/static/images/course_management.png)

Project presentation slides and a customer-facing demo video
readme.md file with clear instructions

Unit tests for database API methods
![Unit Test](app/static/images/unit_test.png)

### What We Were in the Middle of Implementing
Source Documentation and auto-generated documentation files


### What We Planned for the Future
User profile/course images: upload and edit images
Username, email, and password: input data validation / retrieve forgotten password / automatic username generation / change username
Expand admin operations: ban users, give or remove admin privileges, delete flagged reviews / delete courses
More review features: leave comments on each review / delete one’s own review
Search filters for courses & reviews: set filters for advanced search / sort reviews
Better responsiveness for smaller screens: adaptable to phone and tablet screens
Increase database resilience: make the database more defensive against invalid user input, may consider migrating the database to postgres if such needs arise


### Known Problems and Limitations
Unlimited upvotes and downvotes: we will need to update the SQL table design
The server crashes when a new user signs up with a duplicate username: because username is defined as Unique in the Users table; we will need graceful front-end handling
Password: currently password is not hashed; we will need to implement more rigorous password handling

## System Overview
CSPB Review uses the following stack:
- Frontend: HTML/CSS
- Backend: Flask and Python
- Database: Currently sqlite (Future PostgreSQL)
The system was designed to support incremental development, clear separation of
concerns, and straightforward testing.

## Pages That Access Database Information
- **Login/ Sign Up**: users
	- verify credentials or add a new user to database
- **Home**: courses, users, review 
- personalized welcome message and navigation bar
- recent review section
- **Admin Add/Edit Course**: courses
	- add or edit a course and its attributes to the database
- **Admin Panel**: courses, users, reviews 
- admin panel manages all tables in database
- **Submit/Edit Review**: courses, users, reviews 
- tie a user and their review to a specific course
- **Profile**: courses, users, reviews
- profile info
- recent review section
- **Update User Info**: users
- update user’s password
- **Courses (Browse)**: courses, reviews
- list all courses and average ratings
- **Course Details**: courses, users, reviews
- list the course info and all reviews with the review author

## Page Data Access Tests (High-Level)

### Use case name
Home page loads current data for the logged-in user

### Description
Verify the home page displays the logged-in username and the most recent reviews 

### Pre-conditions
- User account exists
- User is logged in
- The database has course reviews

### Test steps
1. Navigate to the Home page
2. Observe the Welcome message
3. Observe the list of reviews

### Expected result
- The welcome message shows the logged-in user’s username.
- The list of reviews displays the most recently written reviews, including course names, rating, difficulty, workload, review text, year & semester, upvote, downvote.

### Actual result
- Home page shows all the expected data

### Status
Pass

### Notes
N/A

### Post-conditions
No data is modified.

_______________________________________

### Use case name
Submit a user-written course review to the platform

### Description
Verify that a user can submit a review, the review is inserted to the database, and the platform can retrieve this review

### Pre-conditions
- User account exists
- User is logged in
- The database exists
- The course exists


### Test steps
1. Navigate to the Submit Review page.
2. Write a review and submit.
3. Navigate to the Home page or the Course Details page of the reviewed course.

### Expected result
- The Submit Review page can take user input data.
- The Home Page or the Course Details page shows the review just submitted.

### Actual result
- The platform shows the review this user just submitted.

### Status
Pass

### Notes
N/A

### Post-conditions
The user-written course review is inserted to the database.

________________________________________

### Use case name
Add a new course to the platform

### Description
Verify that an administrator can add a course to the platform and users can write a review for the added course

### Pre-conditions
- Administrator account exists
- Administrator is logged in
- The database exists

### Test steps
1. Navigate to the Profile page.
2. Navigate to the Admin Panel page.
3. Navigate to the Add Course page.
4. Add a course and submit
5. Navigate the Browse page.
6. Write a review for the added course.


### Expected result
- An administrator can access the Add Course page and can add a new course to the platform. 
- The Browse page shows the newly added course.
- Users can write reviews for this course.

### Actual result
- An administrator can add a course. 
- The platform shows the new course.
- Users can write reviews for this course. 

### Status
Pass

### Notes
N/A

### Post-conditions
The new course is inserted to the database.


## Reflection
This project provided valuable hands-on experience with designing, building, testing, deploying, and presenting a full-stack web application. Throughout the project, our team learned not only technical skills but also the importance of communication, collaboration, planning, and adaptability.
Key Takeaways
###Scope Control and MVP
- Focusing on the Minimum Viable Product (MVP) helped keep the project manageable and ensured that we were able to deliver the core features within the semester.
- Prioritizing essential functionality prevented the team from becoming overwhelmed by additional features.
###Technical Dependencies and Time Zones
- Many tasks depended on other components being completed first. For example, database and back-end functionality often needed to be completed before certain front-end features could be fully implemented.
- Waiting for pull requests to be reviewed and merged also occasionally affected development progress.
- Different time zones made coordination more challenging.
- Mitigation: Weekly team meetings and frequent communication through Discord helped us coordinate dependencies and keep everyone updated.
###Team Collaboration
- Team members had different work styles, technical backgrounds, and levels of experience.
- We divided tasks based on individual strengths while helping one another when challenges arose.
- Clear task ownership, regular communication, and weekly check-ins helped maintain steady progress.
###Time Management
- Our actual development period was less than one month, which made the final weeks of the project especially intense.
- In retrospect, completing the design phase earlier and beginning implementation sooner would have provided more time for development, integration, and testing.
### Collaborative Learning and Problem Solving
- Although team members had different skill sets and experience levels, everyone was willing to help when someone encountered a difficult concept or technical problem.
- Working together allowed us to troubleshoot problems more efficiently and learn from one another throughout the project.
###Overall Learning Experience
- Despite initially being unfamiliar with some of the technologies and tools, we successfully implemented the project's core features.
- The project gave us practical experience with the complete software development lifecycle, including planning, design, implementation, version control, integration, testing, deployment, and presentation.
- Most importantly, we learned how to transform an initial idea into a functional and scalable software prototype
###Deployment and Integration: Each team member tested their assigned features locally before submitting and merging their changes. This helped us catch individual issues early, while integration testing helped ensure that features developed by different team members worked correctly together. Deploying the application also taught us that something working locally does not always mean it will work the same way in a production environment. Frequent testing and integration helped us identify problems earlier and reduced surprises near the end of the project.
