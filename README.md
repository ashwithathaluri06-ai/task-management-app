# Task Management Application

A full-stack Task Management Application built using Flask, SQLite, HTML, CSS, and JavaScript.

The application allows users to securely register and log in, create and manage their personal tasks, and track task completion through a responsive web interface.

## Features

* User registration
* Secure user login
* Password hashing
* User logout
* User-specific task management
* Create tasks
* View tasks
* Edit tasks
* Delete tasks
* Mark tasks as completed
* Undo completed tasks
* Filter tasks by:

  * All
  * Pending
  * Completed
* Responsive design for different screen sizes
* REST-style API integration
* SQLite database
* Authentication and authorization using Flask-Login

## Technologies Used

### Backend

* Python
* Flask
* Flask-SQLAlchemy
* Flask-Login
* Werkzeug

### Frontend

* HTML5
* CSS3
* JavaScript

### Database

* SQLite

## Project Structure

```text
task-managment/
│
├── app.py
├── README.md
│
├── instance/
│   └── tasks.db
│
├── static/
│   ├── script.js
│   └── style.css
│
└── templates/
    ├── index.html
    ├── login.html
    └── register.html
```

## How It Works

1. A new user creates an account through the registration page.
2. The password is securely hashed before being stored in the database.
3. The user logs in using their credentials.
4. After authentication, the user is redirected to the task dashboard.
5. Users can create, view, edit, complete, undo, and delete their own tasks.
6. Each task is associated with the logged-in user's account.
7. Authentication and authorization prevent users from accessing another user's tasks.

## API Endpoints

| Method | Endpoint               | Purpose                             |
| ------ | ---------------------- | ----------------------------------- |
| GET    | `/api/tasks`           | Retrieve the logged-in user's tasks |
| POST   | `/api/tasks`           | Create a new task                   |
| PUT    | `/api/tasks/<task_id>` | Update a task                       |
| DELETE | `/api/tasks/<task_id>` | Delete a task                       |

## Installation

Clone the repository and open the project folder.

Install the required dependencies:

```bash
pip install flask flask-sqlalchemy flask-login werkzeug
```

Run the application:

```bash
python app.py
```

Open the application in a browser:

```text
http://127.0.0.1:5000
```

## Security

The application uses:

* Password hashing with Werkzeug
* Flask-Login for session-based authentication
* User-specific database queries
* Authorization checks for task operations

Users can only access and modify tasks associated with their own account.

## Future Improvements

Possible future enhancements include:

* Task due dates
* Task priorities
* Categories and tags
* Search functionality
* Pagination
* Improved error messages
* Real-time task updates using WebSockets
* Deployment to a cloud platform

## Internship Project

This project was developed as part of the **Thiranex Full Stack Internship**.

### Project Objective

To build a functional full-stack task management application demonstrating:

* Frontend development
* Backend development
* Database integration
* REST API usage
* Authentication and authorization
* CRUD operations
* Responsive web design
* Dynamic data handling
