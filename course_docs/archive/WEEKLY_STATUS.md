# WEEKLY_STATUS.md

## Project Milestone 3: Weekly Status Report

**Project:** CSPB Course Review Platform

**Team Number:** 8

**Team Name:** Team Infinity

---
## Overview
This document captures the **weekly status** of the **CSPB Course Review Platform** project for the specified reporting period.
It is intended to provide a concise snapshot of progress, plans, and risks, and
will be updated weekly throughout the project.
This weekly status format is designed to:
- Track ongoing progress over time
- Surface risks and blockers early
- Provide accountability for individual contributions
- Supplement the project management tool used by the team
---

## Project Management Snapshot
The team is using a shared **Trello board** to manage tasks and sprint progress.
At the time of this report:
- Columns include: Backlog, In Progress, In Review, Done
- Tasks are assigned to individual team members
---

# Reporting Period

**Week:** 7 (of the semester)

**Sprint**: 3

**Meeting Held:** Yes

**Meeting Date:** July 2, 2026

**Meeting Duration:** 45 minutes

**Meeting Format:** Discord

**Scrum master:** Ching-Hsiang (Sean) Lin

**Meeting attendees:** All team members

---

## Progress Since Last Week
This week, the team focused on **initial project setup and scope definition**.
Major infrastructure and planning milestones were completed to prepare for active
development.
Key accomplishments include:
- Defined MVP feature scope
- Agreed on the feature set of each required page
- Created a Flask skeleton and a set of routes to implement
- Agreed on the essential workflow of login and review writing
---

## Completed Tasks
- Product scope
    - Clarified the required feature set: login, signup, adding reviews, adding courses
    - Added more wireframe sketches: guest homepage and admin panel
    - Added flowcharts to illustrate home page, login, and review writing workflow 
    - Defined the scope of a minimum viable product
- Repository
    - Created a Flask skeleton
    - Defined a set of routes to be implemented
---

## Planned Tasks for Next Week
- Begin frontend page layout design
- Determine user interface elements for each page
- Design the initial database schema corresponding to the frontend design  
- Determine how pages link to each other
- Expand on basic backend routes for users
---

## Blockers and Issues
No major technical blockers were encountered this week.
One discussion point involved balancing MVP scope versus optional enhancements. The
team agreed to:
- Resist the temptation to add more features before implement core features
- Defer more advanced features such as admin moderation until time permits
---

## Risks and Mitigation
**Identified Risk:** Potential feature creep
- *Mitigation:* Strict adherence to MVP scope and milestone requirements
- *Mitigation:* Focus only on a short list of CSPB courses and the current set of essential features
- *Mitigation:* identify must-have features and nice-to-have features

**Identified Risk:** Potentially code conflicts
- *Mitigation:* Everyone should create a branch for development while working on part of the project. Avoid pushing directly to the main branch without peer review.  
---

## Team Reflection
The team reported:
- The brainstorming sessions have been going well.
- Collaboration on the same project repository requires clear workflow and branch management.
- The current repository structure can be further improved for better structure and division of work.
The weekly status format was found to be useful for maintaining accountability and
focus.
---
## Individual Contributions This Week
- **Hannah Pfeifer:** Set up initial backend app with placeholders using Flask in repo, added .gitignore file to repo, contributed to software specifications and questions to resolve on Google Doc, added tasks to Trello board, set up initial weekly status document
- **Adam Chathankeo:** Contributed to software specifications on Google Doc, added tasks to Trello board
- **Craig Sanders:** Contributed to software specifications on Google Doc
- **Ching-Hsiang (Sean) Lin**: Coordinated meeting agenda, added pages for guest home page and admin panel, and added flowcharts
---

## Reporting Period

**Week**: 8 (of the semester)

**Sprint**: 4

**Meeting Held:** Yes

**Meeting Date:** July 9, 2026

**Meeting Duration:** 25 minutes

**Meeting Format:** Discord

**Scrum Master:** Adam Chanthakeo

**Meeting Attendees:** All team members

## Progress Since Last Week
This week, the team focused on the **finalization of project setup and scope definition**. Major planning milestones were completed to prepare for active development.

Key accomplishments include:
- Created visual mockups within our MVP scope
- Improved understanding of the application flow and features
- Agreed on the essential workflow of login and review writing
- Agreed on the set number of courses to use in the database
---

## Completed Tasks
- Product scope
    - Finalized feature set: login, signup, adding reviews, adding courses
    - Completed wireframe sketches for the guest homepage and admin panel
    - Added flowcharts to illustrate the home page, login, and review writing workflow
    - Defined the scope of a minimum viable product
- Repository
    - Created a Flask skeleton
    - Defined a set of routes to be implemented
- SQL Database
    - Discussed which courses to use to create mock data in the database
---

## Planned Tasks for Next Week
- Begin frontend page layout design
- Determine user interface elements for each page
- Design the initial database schema corresponding to the frontend design
- Determine how pages link to each other
- Expand on basic backend routes for users

---

## Blockers and Issues
No major technical blockers were encountered this week.

One discussion point involved providing individualized tasks to each team member. The team agreed to:
- Meet in the middle of the week to determine who can complete which tasks (such as HTML pages or the SQL database)
- Ensure we maintain communication even when it is not meeting time
---

## Risks and Mitigation

**Identified Risk:** Overcomplicating the pages and being unable to complete all tasks in a timely fashion
- *Mitigation:* Strict adherence to MVP scope and milestone requirements while re-evaluating which features are required each sprint
- *Mitigation:* Limit the project to three courses for example data
- *Mitigation:* Assign designated tasks to each team member

**Identified Risk:** Potential code conflicts
- *Mitigation:* Everyone should create a branch while working on their part of the project. Avoid pushing directly to the main branch without peer review.
---

## Team Reflection
The team reported:
- The overall project idea has been solidified.
- Collaborating on the page designs required the team to rethink the minimum viable product and determine what features are necessary within the project timeline.
- There is potential to expand and continue collaborating on this project in the future.

The weekly status format was found to be useful for maintaining accountability and focus.

---

## Individual Contributions This Week
- **Hannah Pfeifer:** Created the login and course page testing markdown documentation and added tasks to the Trello board.
- **Adam Chanthakeo:** Assisted with page testing for the login and review account pages, added tasks to the Trello board, served as Scrum Master, and submitted the assignment.
- **Craig Sanders:** Contributed pages to the page testing document and created rendered mockup images.
- **Ching-Hsiang (Sean) Lin:** Contributed pages to the page testing document, created rendered mockup images, and reviewed pages to identify any missing information.
---

## Notes
This file will be updated weekly as the project progresses.
Earlier weekly entries may be retained below or moved to an archive directory if
the file grows large

---

# Reporting Period

**Week**: 9 (of the semester)

**Sprint**: 5

**Meeting Held:** Yes

**Meeting Date:** July 16, 2026

**Meeting Duration:** 20 minutes

**Meeting Format:** Zoom

**Scrum master:** Hannah Pfeifer

**Meeting attendees:** All team members

---

## Progress Since Last Week
This week, the team focused on **Milestone 5 and SQL Design**.
Major infrastructure and planning milestones were completed to prepare for active
development.
Key accomplishments include:
- Discussed progress of project, confirming all requirements for Milestone 5 were met
- Agreed on the SQL table contents and access methods
- Updated Flask routes and started on HTML pages
- Discussed project deadlines and goals for next week
---

## Completed Tasks
- Milestone 5
    - Defined 3 required tables: Users, Courses, and Reviews
    - Defined access methods and how to test them
    - Decided that commenting will not be included in the MVP due to time constraints
    - Discuss submission of SQL_TESTING.md
- Repository
    - Expanded on Flask skeleton
    - Completed base.html from which the rest of the html pages will extend from
---

## Planned Tasks for Next Week
- Continue frontend page layout designs
- Implement the initial SQL tables and queries
- Research and implement some HTML web forms so users can submit information to the database
- Make classes for course and review objects
---

## Blockers and Issues
No major technical blockers were encountered this week.

---

## Risks and Mitigation
**Identified Risk:** Only 3 weeks before project demo
- *Mitigation:* Focus on functionality rather than aesthetics for upcoming project demo.

**Identified Risk:** Potential duplicate work
- *Mitigation:* Everyone will work on a separate task such as SQL, web forms, or HTML. In our Google Doc, we will create a list of html pages and who is working on what so our work doesn't overlap.
---

## Team Reflection
The team reported:
- The planning stage is mostly complete (will add items as needed) so now focus should be on implementing and tying everything together.
---

## Individual Contributions This Week
- **Hannah Pfeifer:** Expanded routes on backend app using Flask, contributed to SQL table design on Google Doc, added HTML and variables planning page to Google Doc, built base.html and started working on home.html, updated WEEKLY_STATUS.md.
- **Adam Chathankeo:** Contributed to SQL design on Google Doc, formatted and submitted Milestone 5, working on simple css styling for html files, and reviewing flask skeleton, reviewed WEEKLY_STATUS.md.
- **Craig Sanders:** Contributed to SQL access methods and testing on Google Doc.
- **Ching-Hsiang (Sean) Lin**: Contributed to SQL tables, testing, and access methods on Google Doc.
---

# Reporting Period

**Week**: 10 (of the semester)

**Sprint**: 6

**Meeting Held:** Yes

**Meeting Date:** July 23, 2026

**Meeting Duration:** 20 minutes

**Meeting Format:** Zoom

**Scrum master:** Hannah

**Meeting attendees:** Hannah, Adam, Sean

---

## Progress Since Last Week
This week, the team focused on **Project progress and planning before demo**.

Key accomplishments include:
- Built out more HTML and CSS on the frontend
- Started building out SQL database
- Discussed project deadlines and goals for next week including completing main functionality by end of next week to allow time for testing before the Aug. 6th presentation demo
- Decide users will login with email instead of username
---

## Completed Tasks
- Repository
    - Expanded on HTML and CSS
    - SQL database created and methods started
    - Added necessary funtions added for submit_review.html 
---

## Planned Tasks for Next Week
- Adam and Hannah - Finish building out the HTML and CSS pages
- Sean - Finish the SQL methods and test them to ensure they work correctly
- Sean - Double the initial test data in the database tables
- Sean - Create a unit test for the database functions
- Sean - Create a list of SQL functions/methods in the Google Doc for reference
- Sean - Work on creating the login system and hook it up with the login page
- Hannah - Look into Flask sessions for login/logout functionality
- Sean - show team how to pull data from the database into a webpage
- Adam and Hannah - Finish building HTML web forms so users can submit information to the database
- Craig - Work on testing submit_review and interfaces with DB. 
- Craig - Start the classes for Review and Course which will be how we instantiate the Course and relevant Reviews after querying the DB.
---

## Blockers and Issues
No major technical blockers were encountered this week.

---

## Risks and Mitigation
**Identified Risk:** Only 2 weeks before project demo
- *Mitigation:* Try to finish as much as possible in the next week so we can leave the last week for testing and preparing for the demo.
---

## Team Reflection
The team reported:
- Frontend and backend is coming along and we will soon need to tie everything together. We might need an additional check in meeting this weekend or early next week to touch base. We will keep open communication in the Discord chat when we finish something.
---

## Individual Contributions This Week
- **Hannah Pfeifer:** Expanded on HTML pages and finished About and Home pages. Built out style.css for overall website styling. Updated WEEKLY_STATUS.md.
- **Adam Chathankeo:** Worked on CSS styling for html files. Finished HTML for Login and Sign Up pages.
- **Craig Sanders:** Submitted submit_review.html with the necessary functions in app.py and models.py
- **Ching-Hsiang (Sean) Lin**: Build SQL database and sample courses and reviews. Added SQL methods. 
---
