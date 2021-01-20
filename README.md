# Simple Ticketing

### Foreword - CS50

This project is the final project of the CS50 class. This class is an introduction to computer science at Harvard and is available through the edX platform. 

The goal of this project is to develop a piece of software that uses technologies learned through the class. The nature of the project is entirely left to the student.

## Description of the need /problem to solve

In previous professional projects, I had a need for a feedback system for digital tools I developed. I would usually receive notes, calls, emails or even oral comments from the users and had to find a way to keep track of those, prioritize and let users know when the issue they raised was solved and how.

My goal for this project is to create a ticketing system as simple as possible, both for he admins and users.

### Known and existing solutions

#### Microsoft Excel

The most basic implementation is to set up a MS Excel file, with several columns and filters to help retrieve the data and research a specific issue. That file can be shared so that users can fill in directly an issue they'd like to report or to check the progress of an issue that was previously opened. Using some VBA code, it is possible to add more functions and make easier the input, search and display of information.

This solution is fairly easy to implement but has several drawbacks : 

* sharing one file with several users induces risks of errors & data loss, it makes it more difficult for users to retrieve the data    
* follow up and updates is made difficult if file shared between users/projects
* issues management made difficult if different Excel file for each project
* most of the functions not provided by Excel have to be implemented with VBA code

#### 3rd party softwares

An other solution to the problem is to use a 3rd party app that provide professional solutions with a lot of options. These have also some drawbacks : 

* price of licenses
* too complex, expensive, considering the need
* too many functionalities can make set up and get familiar with difficult
* another program to install for each user



## Simple Ticketing

The goal of this project is to implement a ticketing system that is simple to use and has only necessary features. The service is web based and can be shared as a link. it doesn't need to install any piece of software and doesn't need any training nor user manual for the users.

This project is focused on the user functionalities described hereafter. In a second project (hopefully part of the Web Programming with Python and Javascript CS50 Class), I will focus on the administrator functionalities (configuration, implementation) and management of multiple projects.

The final goal is to have a ticketing system that an admin can setup, configure and share easily. The backend allows the admin to manage the ticketing system of several projects. The front end is a user friendly and efficient way for users to give feedback.

## Features

### User

* [x] __register__ : create an account with email and password 
* [x] __log in__ : welcome page shows opened tickets and stats (stats tbd)

* [x] __drop a ticket__ on a project from drop down menu (users can drop tickets on any project)
* [x] __look up__ : history of his own tickets
* [x] __look up__ : a ticket by # (if ticket is his own)
* [x] __edit__ a ticket (if ticket is his own)
* [x] __log out__

### Admin

* [x] __log in__, welcome page shows list of open projects
* [x] __create__ projects
* [x] __drop a ticket__ on any project
* [x] __look up__ history of tickets (tbd : search/filter/sort criteria to ease tasks)
* [x] __look up__ a ticket by # (any ticket)
* [x] __edit__ a ticket (any ticket)
* [x] __log out__

### Other features : 

* [x] __click/link__ on a ticket to see history of the ticket (when viewing a list of tickets)
* [x] __click/link__ on a ticket to edit ticket (when viewing a list of ticket)
* [x] __click/link__ to edit a ticket displayed in the lookup view

### Future Features

The next features will be developed in future versions of the project.

* [ ] email opt in/out to receive updates on tickets (observer pattern) / make sure email address is correct
* [ ] search/sort/filters to ease navigation among tickets (both admin/users)
* [ ] welcome page with stats for admin (number open/closed tickets, time to process a ticket, tickets per person/project/category/week/day,..)
* [ ] language french/english using a config file (+ option for preferred language for users, or switch in the menu)
* [ ] admin : waiting list of tickets to work on (+ new role and possibility to assign tickets for users to solve)

## Technologies

For this project, I used the same technologies as in the "finance" project from the CS50 Class.

* __CS50 IDE__ : this online IDE based on Cloud9 by AWS provides a development environment that is convenient to use
* __CS50 libraries__ : the SQL library from CS50 makes easier the use of the 
* __Flask__ is the framework used for the web application
* __Python__ is the programming language used with Flask
* __SQLite, SQL, phpliteadmin__ are the database, language and db admin tool used to store and request the date.
* __Werkzeug__ is used to handle exceptions and security (generate and check password hashes)
* __HTML, CSS, javascript, jinja and bootstap__  have been used to create templates and webpages



### Bases and tables

| Tables   | Description                                                |
| -------- | ---------------------------------------------------------- |
| tickets  | tickets created                                            |
| jobs     | any modification of a ticket                               |
| projects | list of existing projects for which tickets can be created |
| users    | registered users                                           |

#### tickets

| Field    | Description                                             |
| -------- | ------------------------------------------------------- |
| id       | ticket id                                               |
| project  | project id                                              |
| date     | dateof ticket opening                                   |
| username | username of user opening the ticket                     |
| status   | status of the ticket (updated each time a job is added) |

#### jobs

| Field       | Description                         |
| ----------- | ----------------------------------- |
| id          | job id                              |
| ticket      | ticket id for that job              |
| date        | date                                |
| username    | username of user doing the job      |
| description | description of the job              |
| status      | status of ticket once job completed |

#### users

| Field    | Description     |
| -------- | --------------- |
| id       | id              |
| username | user name       |
| hash     | hashed password |
| email    | email adress    |
| role     | user's role     |

#### projects

| Field | Description  |
| ----- | ------------ |
| id    | project id   |
| name  | project name |



## Future developments

Some future features have already been mentioned. Future developments will also focus on the following topics : 

#### Structure

Organization and reuse of code could be improved. Several functions and pages are similar enough to be properly reworked, using more helper functions and making a good use of the MVC pattern. 

An example is page showing tickets (history or open tickets) : this page should be made of only one form, but displaying different data and options depending on the user. An admin will have a filter to select a username and only see those tickets and updates, while a user will see this filter as disabled and set with his own name.

#### View

A basic use is made of bootstrap, jinja and CSS. The html templates could be reworked and improved, and the overall aesthetic and responsiveness improved. 

####  Implementation

Another focus of the next developments will be the implementation of the simple ticketing tool. Right now it is working fine on the Amazon Cloud9 platform, but the aim is for anyone to be able to deploy it in a couple clicks and this will be the focus of the next part of the project.

#### Data Structure

The data structure and tables can be reengineered in order to facilitate some of the requests and display of information. 

Also it could be interesting to be able to import/export raw data or to generate a report of all the tickets and updates for a specific project, as part as the documentation of the project. 
