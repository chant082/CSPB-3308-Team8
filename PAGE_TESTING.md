# 1) Course Browse Page (Guest & Logged-In)

## Page Title
CSPB Course Reviews

## Page Description
Purpose: Shows a list of courses with basic information such as course names, credits, ratings, difficulties, workloads. Guests can browse courses without an account. They can also sign up or log in.

**Mockup**
*Guest view:*

*Logged in user view: *

## Parameters Needed for the Page
- Route params: none
- Query params: none

## Data Needed to Render the Page
- login state - not logged-in
- Course names
- Credits
- Average ratings
- Average difficulties
- Average workloads
- Core/Elective tags
- Prerequisites (if time permits)

## Link Destinations for the Page
Log In -> login page
Sign Up -> signup page

## Tests for Verifying Rendering of the Page
The page title appears correctly
The list of courses appears
Course names appear
Course credits appear
Course ratings, difficulties, workloads appear
Course tags appear
Course prerequisites appear (if time permits)

# 2) Home Page (Regular user)

## Page Title
CSPB Course Reviews

## Page Description
Purpose: Shows a welcome message for a logged-in regular user. The user can write a review, browse courses, view recently reviewed courses, and log out.
When logged in, an admin can see the Admin Panel option on the drop-down list

**Mockup**
*Regular user view:*

*Admin view:*

## Parameters Needed for the Page
- Route params: none
- Query params: none

## Data Needed to Render the Page
- Login state : logged-in
- User role: regular / admin 
- Username
- Recently reviewed courses by the user

## Link Destinations for the Page
Write a Review -> Review writing page
Log Out -> Course Browse page (guest view)
Browse -> Course Browse page (regular user)
Admin Panel -> Admin Panel page

## Tests for Verifying Rendering of the Page
The page title appears correctly
The list of recently-reviewed courses appears
Write a Review button appears
Username appears
Home button appears
Browse button appears
Drop-down list appears
Log Out button appears
Admin Panel button appears

---

# 3) Login Page

## Page Title
Login

## Page Description
Allows registered users to log into the application using their username and password.

**Mockup**

## Parameters Needed for the Page
- Route Parameters: GET /login, POST /login
- Query Parameters: optional ?next=/classes/<class for review>

## Data Needed to Render the Page
- Username and password input
- Error message if login fails
- User info from database to verify credentials
- Session object that stores user_id after successful login

## Link Destinations for the Page
- CSPB Course Reviews Logo → ‘/home’ - Home page(guest view)
- Login success → `/dashboard` - User dashboard
- Sign up → `/signup` - create an account
- Forgot password → `/reset-password` (optional)

## Tests for Verifying Rendering of the Page
1. **Form elements render**
   - Login page loads successfully 
   - Email and password fields are displayed
   - Links work correctly
2. **Validation**
   - Empty submit shows validation messages
3. **Auth success flow**
   - Successful login stores token and navigates to `/dashboard` (or redirect)
4. **Auth failure flow**
   - Invalid credentials display error banner/message and remain on page
5. **Dashboard cannot be accessed without logging in

---

# 3) Admin Panel (Courses)

## Page Title
Admin Panel

## Page Description
Purpose: Provide a panel for an admin to add, edit, and delete courses

**Mockup**




## Parameters Needed for the Page
- Route params: none
- Query params: none

## Data Needed to Render the Page
- Login state : logged-in
- User role: admin 
- Username
- Available courses in the database
- Data of each course

## Link Destinations for the Page
Add Course -> Course adding page
Edit Course -> Course adding page
Delete Course -> Confirmation message for course deletion
Log Out -> Course Browse page (guest view)
Browse -> Course Browse page (regular/admin user)
Admin Panel -> Admin Panel page

## Tests for Verifying Rendering of the Page
The page title appears correctly
The list of recently-reviewed courses appears
Add Course button appears
Edit Course button appears
Delete Course button appears
Username appears
Home button appears
Browse button appears
Drop-down list appears
Log Out button appears
Admin Panel button appears


# 4) Admin Panel (Users)

## Page Title
Admin Panel

## Page Description
Purpose: Provide a panel for an admin to monitor users

**Mockup**

## Parameters Needed for the Page
- Route params: none
- Query params: none

## Data Needed to Render the Page
- Login state : logged-in
- User role: admin 
- Username
- Available users in the database
- Data of each user

## Link Destinations for the Page
Delete Course -> Confirmation message for course deletion
Log Out -> Course Browse page (guest view)
Browse -> Course Browse page (regular/admin user)
Admin Panel -> Admin Panel page

## Tests for Verifying Rendering of the Page
The page title appears correctly
The list of recently-reviewed courses appears
Add User button appears
Edit User button appears
Delete User button appears
Username appears
User ID appears
User role appears
Last Logged time appears
Home button appears
Browse button appears
Drop-down list appears
Log Out button appears
Admin Panel button appears

---

# 5) Add/Edit Course 

## Page Title
Add Course / Edit Course

## Page Description
Purpose: Allows an admin to add a new course or to edit an existing course


**Mockup**
*Add new course*

*Edit course*




## Parameters Needed for the Page
- Route params: none
- Query params: none

## Data Needed to Render the Page
- Login state : logged-in
- User role: admin 
- Username
- Available courses in the database
- Data of the selected course

## Link Destinations for the Page
Add Course -> Insert course data to the database
Log Out -> Course Browse page (guest view)
Browse -> Course Browse page (admin user)
Admin Panel -> Admin Panel page
Cancel -> Admin Panel page

## Tests for Verifying Rendering of the Page
The page title appears correctly
Empty text fields appear when adding a new course
Filled text fields with course data appear when editing an existing course
Add Course appears when adding a course
Update Course appears when adding a course
Course name text field appears
Credit drop-down list appears
Description text field appears
Core/Elective radio buttons appear
Username appears
Home button appears
Browse button appears
Drop-down list appears
Log Out button appears
Admin Panel button appears

---

# 6) Create Account

## Page Title
Create Account

## Page Description
Purpose: Allow a user to create an account by putting their CU Boulder email address, input a unique username, and choose a password password

**Mockup:**


## Parameters Needed for the Page 
- Route params: none 
- Query params: none

## Data Needed to Render the Page
- Auth state:
  - User is not logged in.
- API data:
  - `POST /api/auth/register` → Create a new user account.
- UI state:
  - Full Name
  - Username
  - Email
  - Password
  - Form validation errors
  - Loading state while creating account

## Link Destinations for the Page
- Sign Up → Creates the account and redirects to `/login`
- Log In → `/login`
- About → `/about`
- Contact → `/contact`
- Privacy → `/privacy`

## Tests for Verifying Rendering of the Page
1. **Form renders**
   - Full Name, Username, Email, Password fields, and Sign Up button are displayed.

2. **Required fields**
   - The form cannot be submitted if any required field is empty.

3. **Username validation**
   - Username must be unique and display an error if already taken.

4. **Email validation**
   - Only valid CU Boulder email addresses are accepted.

5. **Password validation**
   - Password must meet the minimum length requirement.

6. **Successful account creation**
   - A valid submission creates the account and redirects the user to the Login page (or Dashboard if automatic login is implemented).

7. **Duplicate account handling**
   - Attempting to register with an existing email or username displays an appropriate error message.

# 7) Review Account

## Page Title
Review Account

## Page Description
Purpose: Allow a logged-in user to review their account information and change their password.

**Mockup:**



## Parameters Needed for the Page
- Route params: none
- Query params: none

## Data Needed to Render the Page
- Auth state:
  - User is logged in.
- API data:
  - `GET /api/user/profile` → Retrieve the user's account information.
  - `PUT /api/user/password` → Update the user's password.
- UI state:
  - Full Name
  - Username
  - Email
  - Member Since
  - Change Password button
  - Current Password
  - New Password
  - Confirm Password
  - Form validation errors
  - Loading state while updating password

## Link Destinations for the Page
- Home → `/`
- Browse → `/browse`
- Change Password → Displays the password update form
- Save Password → Updates the user's password
- Cancel → Closes the password update form

## Tests for Verifying Rendering of the Page
1. **Account information renders**
   - Full Name, Username, Email, Member Since, and Change Password button are displayed.

2. **Password form**
   - Clicking Change Password displays the Current Password, New Password, and Confirm Password fields.

3. **Required fields**
   - The password form cannot be submitted if any required field is empty.

4. **Password validation**
   - New Password must meet the minimum length requirement.
   - Confirm Password must match the New Password.

5. **Successful password update**
   - A valid submission updates the password and displays a success message.

6. **Incorrect current password**
   - Entering an incorrect current password displays an appropriate error message.

7. **Loading state**
   - The Save Password button is disabled while the password update request is processing.

8. **Authentication**
   - Users who are not logged in are redirected to the Login page.



# 8) Course Page

## Page Title
*Course Title* (Fills in with a specific course title)

## Page Description
Displays information for a selected course, including its average ratings and all submitted student reviews. Users can read reviews, upvote or downvote reviews, add comments, and navigate to write a review for the course.

**Mockup:**






```
Header (logo, nav bar, profile/login icon)
Course number and title
Average star rating
Average difficulty
Average time taken
Write a Review
List of reviews
filter highest to lowest average rating, most helpful, semester, year
Each review shows: 
reviewer’s username
Ratings
semester/year taken
review text
upvote/downvote button with counts
Comments
Add comment button
flag/report button 
Mockup:

+------------------------------------------------------------------------------------------------+
| [Logo] Course Reviews    Home   Browse   Search        [Profile/Login] 	|
+------------------------------------------------------------------------------------------------+
| CSPB 3308 - Software Development                               			 |
| "Fundamentals of software development and tools”			 |
|  		                                                   				 |
|--------------------------------------------------------------------------------------------------|
|  ★★★★☆ 4.2/5        Difficulty: 3.6/5        Avg Time: 8 hrs/wk      		 |
|  (based on 42 reviews)                                                 			 |
|--------------------------------------------------------------------------------------------------|
|                          [ Write a Review ]                          				|
+------------------------------------------------------------------------------------------------+
| Reviews                                                               				|
| Sort by: [ Highest Rated v ] [ Most Helpful ] [ Semester/Year ]       		|
+------------------------------------------------------------------------------------------------+
| ------------------------------------------------------------------ —---------------------------|
| | jsmith22                              Fall 2025                 			          | |
| | ★★★★★  Difficulty: 4/5   Time: 10 hrs/wk                        	          | |
| |                                                                    			          | |
| | "Tough but rewarding. The professor explains recursion really               | |
| | well, just be ready to put in the hours on problem sets."                         | |
| |                                                                                                                  | |
| | [▲ 14]  [▼ 2]        [ Flag/Report ]                                                             | |
| |                                                                                                                  | |
| |   Comments (3)                                     [ Add Comment]                         | |
| |     • alex_r: "Totally agree about the problem sets"                                  | |
| |     • kt_2024: "Which semester was this?"                                               | |
| ------------------------------------------------------------------------------------------------- |
|                                                                        				|
| ------------------------------------------------------------------------------------------------ |
| | maria_p                                Spring 2025               			| |
| | ★★★☆☆  Difficulty: 3/5   Time: 6 hrs/wk                         			| |
| |                                                                  					| |
| | "Decent course, lectures could be more organized."               		| |
| |                                                                  					| |
| | [▲ 5]   [▼ 1]        [ Flag/Report ]                            			| |
| |                                                                  					| |
| |   Comments (0)                                     [ Add Comment]			| |
| ------------------------------------------------------------------------------------------------- |
|                                                                        				|
|                         [ Load More Reviews ]                        			|
+-------------------------------------------------------------------------------------------------+

```

## Parameters Needed for the Page
- Route params: course_id to identify which course to display
- Query params: none

## Data Needed to Render the Page
- Course information (course number, course title, description if available)
- Average course rating, time, and difficulty
- List of reviews for the selected course
- Reviewer username
- Review rating and review text
- Like and dislike counts for each review
- Comments for each review
- User permissions (to determine whether the user can write a review, comment, or like/dislike reviews)

## Link Destinations for the Page
- Home → `/dashboard/<user_id>` if logged in, ‘/home’ if guest
- Browse Courses → `/browse`
- Search Courses → ‘/search’
- Write a Review → /courses/<course_id>/review
- Profile (if logged in) → /profile/<user_id>
- Pages that navigate to course page
	- Browse Courses → selected course page
	- Search Results → selected course page
	- Review Submission → Redirects to the Course Page after successful review
	- Admin Add Course → Redirects to the newly created course page
	- Home/dashboard recent reviews → selected course page

## Tests for Verifying Rendering of the Page
1. **Page elements render**
   - course title, average ratings, reviews for selected course
   - each review displays the reviewer’s username, ratings, semester/year taken, and review text
   - upvote/downvote buttons displayed and update counts correctly
   - comments for each review are displayed correctly
2. **Write Review**
   - Only logged-in and non-admin users can write a review
   - Links opens the review submission page for the selected course
3. **Comment**
   - Only logged-in users can add a comment to a review
4. **Navigation**
   - Selecting a course from Browse Courses and Search opens the correct course page
   - After submitting a review, the user is redirected back to the correct Course Page and the new review appears
   - After creating a new course, the admin is redirected back to the correct Course Page
   - Navigation links from course page direct user to the correct pages
5. **Empty states**
   - If the course has no reviews, a message “No reviews yet. Be the first to review this course!” is displayed

---

## Notes for Implementation
- These pages are intended for **SQL** with a simple top navigation bar.
- Tests can be implemented as:
  - **Manual UI checklist** during development


# 8) Review writing page

## Page Title
*Course Title* (Fills in with a specific course title)

## Page Description
Displays options for year, semester, difficulty, hours per week, overall rating, and comments for the course


## Parameters Needed for the Page
- Route params: none
- Query params: none

## Data Needed to Render the Page
- Login state : logged-in
- User role: regular / admin 
- Username
- Course name
- Course review questionnaire (web form)


## Link Destinations for the Page
Submit -> Confirmation message
Cancel -> Welcome page
Log Out -> Course Browse page (guest view)


## Tests for Verifying Rendering of the Page
The page title appears correctly
The course name appears
Year and semester appear
Difficulty appears
Time spent appears
Rating appears
Text field (comment) appears
Submit button appears
Cancel button appears
