# Flask Task Manager API

This is a simple Flask API for managing tasks. It allows users to create, read, update, and delete tasks.

## Prerequisites

Before you start, make sure you have the following installed:

* Python 3.8 or higher
* Flask
* Flask-SQLAlchemy
* Flask-Migrate
* Flask-JWT-Extended

## Setup

1. Clone this repository to your local machine.
  git clone https://github.com/Nikagagua/flaskRESTfulProject.git
   
3. Create a virtual environment for your project:

python3 -m venv venv


3. Activate the virtual environment:

source venv/bin/activate


4. Install the required dependencies:

pip install -r requirements.txt


5. Create a database file:

touch db.tasks


6. Create a secret key for JWT authentication:

export SECRET_KEY=your_secret_key


## Running the API

1. Start the Flask development server:

flask run

The API will be running on http://localhost:5000.

Documentation
Both an index.html and a pdf file containing the Postman API documentation are accessible.

Endpoints
The API provides the following endpoints:

/: Get the index page for Postman documentation
/login: Login a user and get an access token
/tasks: Get all tasks
/create-task: Create a new task
/update-task/<int:task_id>: Update a task
/delete-task/<int:task_id>: Delete a task
Usage
To use the API, you will need to send requests to the endpoints with the appropriate data. For example, to create a new task, you would send a POST request to the /create-task endpoint with the following data:

json
{
"title": "My new task",
"description": "This is a description of my new task.",
"due_date": "2023-10-04",
"priority": "high",
"status": "pending"
}

The API will return a JSON response with the results of the request. For example, the response for the above request would be:

json
{
"message": "Task created successfully"
}

Authentication
The API uses JWT authentication to protect the endpoints. To access the protected endpoints, you will need to first login a user and get an access token. To do this, you would send a POST request to the /login endpoint with the following data:

json
{
"username": "admin",
"password": "Str0ngPassw0rd"
}

The API will return a JSON response with the access token. For example, the response for the above request would be:

json
{
"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NzU0MzQ3ODAsImlkIjoxfQ.s-21912117eb52c0eb8b9019c3872cb75f"
}

You will need to include this access token in the Authorization header of all requests to protected endpoints. For example, to get all tasks, you would send a GET request to the /tasks endpoint with the following headers:

Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NzU0MzQ3ODAsImlkIjoxfQ.s-21912117eb52c0eb8b9019c3872cb75f

If you have any questions or feedback, feel free to reach out to me: Nikagagua@live.com
