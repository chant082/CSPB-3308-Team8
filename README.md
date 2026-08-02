# Project: CSPB Course Review Platform

___

## **Team Information**

**Team #**: 8

**Team/Product Name**: Team Infinity $\infty$

**Team members:**
- Adam Chanthakeo |
  chant082 |
  Adam.Chanthakeo@colorado.edu

- Hannah Pfeifer |
  hpfeifer37 |
  Hannah.Pfeifer@colorado.edu
  
- Craig Sanders |
  craig-dev-01 |
  Craig.Sanders@colorado.edu
  
- Sean Lin |
  seanlinwriter |
  Ching-Hsiang.Lin@colorado.edu
  
___

## **Project Overview**

**Vision statement**: 

CSPB Course Reviews is a website built to provide reviews for courses offered in the CSPB program at CU Boulder. After sign-up and log-in, students can browse and write reviews for the courses they have taken. They just need to fill out a questionnaire to provide essential information such as course rating, course difficulty, weekly workload, course taken year & semester, and add a review text. Administrators can add & edit courses, manage accounts, and moderate reviews. Guests without accounts can still browse and view reviews but cannot contribute.

**Motivation**: 

For years, CSPB students have had a hard time finding course reviews, which are often scattered and buried in various places, such as Discord, Reddit, Piazza, blogs, and messages. We want to create a platform where students can provide honest feedback about courses in the CSPB program. This will allow students to read course reviews from their peers and make more informed decisions when selecting classes.

**Development method**: Agile/Scrum

**Tech Stack**: Flask, HTML/CSS, SQLite

___

## Setup

**Create a database**

In the terminal, navigate to the *app* directory and run the Python script *create_db*.

This creates SQL tables and populates the tables with initial test data. 

**Reset the database**

To reset the database, run the Python script *reset_db* in the app directory.

This deletes the existing database and then re-creates a new database with initial test data.

Note that all the previously manually added data will disappear.

**Run the app** 

In the *app* directory, run the Python script *app.py*

By default, a Flask application runs on 127.0.0.1:5000

Copy and paste this URL into a web browser to run the app.

## Use the platform

**As a regular user**

Click *Sign Up* on the top-right corner to sign up a user account.

Click *Log In* on the top-right corner to log in to an account.

Click *Browse* to see currently available courses.

When viewing a course, click *Write a Review* to review a course. Specify required information and submit your review. The review will appear on the page of this course. Click *Edit Review* to modify an existing review.

You can also *Upvote*, *Downvote*, and *Report* a review from other users.

On your *Profile* page, you can see the basic information of your account. You can change your password when needed.

**As an administrator**

When you log in as an administrator, you can see *Admin Panel* on your profile page.

On this panel, click *Add Course* and specify required information to add a course to the platform. Users can then add reviews for this course.

You can click *Edit Course* for an existing course to modify course information.

On the Admin Panel, administrators can also view all user accounts and flagged reviews for moderation purposes.