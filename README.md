Django Assignment for Content Managment System

Description:
This Django project is a versatile content management system designed for user registration, role-based authentication, content creation, and search functionalities. 
It provides a user-friendly web interface for managing content, allowing users with different roles to create, edit, and delete their own content. 
Token-based authentication ensures secure access to the APIs, while a comprehensive search feature enables users to find content based on title, body, summary, and categories.

Key Features:
User registration with role-based authentication (Admin, Author).
Token-based authentication for secure API access.
Content creation, viewing, editing, and deletion for Authors.
Search functionality by matching terms in title, body, summary, and categories.
Django Admin panel for managing users and content.

Setup:
Clone the repository: git clone https://github.com/Arunvish987/Arcitech_task/tree/master

Install dependencies:
pip install -r requirements.txt

Run the development server:
python manage.py runserver


API Documentation
-----------------------------Author Side----------------------------------
1. User Registration API
Endpoint: /user_registration_api/
Method: POST

Request Body:
{
    "role_type": 0,  // 0 for Admin, 1 for Author
    "email": "admin1@gmail.com",
    "password": "Admin123",
    "full_name": "Admin One",
    "phone": 9844455555,
    "address": "Shankar Lane",
    "city": "Mumbai",
    "state": "Maharashtra",
    "country": "India",
    "pincode": "400063"
}

Response Body:
{
    "id": 1,
    "role_type": 0,
    "email": "admin1@gmail.com",
    "full_name": "Admin One",
    "phone": "9844455555",
    "address": "Shankar Lane",
    "city": "Mumbai",
    "state": "Maharashtra",
    "country": "India",
    "pincode": "400063"
}

2. User Login API
Endpoint: /user_login/
Method: POST
Request Body:
{
    "email": "admin1@gmail.com",
    "password": "Admin123"
}

Response Body:
{
    "message": "Login successful",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwNDY5MTQ5NSwiaWF0IjoxNzA0NjA1MDk1LCJqdGkiOiIyMWNjMTBmNzQzYmY0NWEzYmVkMzliMTc0NjAwODc2ZCIsInVzZXJfaWQiOjF9.5vsHk001BukDbYFgyBcEwNIgdjYkD2K3LFcAZ4bewq0",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA0NjA1Mzk1LCJpYXQiOjE3MDQ2MDUwOTUsImp0aSI6IjVhMDQ5MTc3YTY0MTQ3MjBiNTk1ODJkZTYwN2VlNjEwIiwidXNlcl9pZCI6MX0.6ezj-y2uvBSwup_hpYYyewx1jQHSD14LaY7l2PA_oi0"
}


3. Search Contents API
Endpoint: /search_contents/
Method: GET
Query Parameters: search_word

Response:
[
    {
        "id": 1,
        "title": "Sample Content",
        "body": "Lorem ipsum...",
        "summary": "A brief summary...",
        "document": "/media/documents/sample_content.pdf",
        "user_type": 1,
        "categories": ["Category 1", "Category 2"]
    },
    // Other matching contents...
]


4. Create Content API
Endpoint: /create_content/
Method: POST

Request Body:
{
    "title": "New Content",
    "body": "Content details...",
    "summary": "A brief summary...",
    "document": "/media/documents/new_content.pdf",
    "categories": ["Category 1", "Category 3"]
}

Response Body:
{
    "id": 2,
    "title": "New Content",
    "body": "Content details...",
    "summary": "A brief summary...",
    "document": "/media/documents/new_content.pdf",
    "user_type": 1,
    "categories": ["Category 1", "Category 3"]
}


5. View Author's Contents API
Endpoint: /view_author_contents/
Method: GET

Response Body:
[
    {
        "id": 1,
        "title": "Sample Content",
        "body": "Lorem ipsum...",
        "summary": "A brief summary...",
        "document": "/media/documents/sample_content.pdf",
        "user_type": 1,
        "categories": ["Category 1", "Category 2"]
    },
    {
        "id": 2,
        "title": "New Content",
        "body": "Content details...",
        "summary": "A brief summary...",
        "document": "/media/documents/new_content.pdf",
        "user_type": 1,
        "categories": ["Category 1", "Category 3"]
    },
    // Other contents...
]


6. Edit Author's Content API
Endpoint: /edit_author_content/
Method: PUT or PATCH

Request Body:
{
    "title": "Updated Content Title",
    "body": "Updated content details...",
    "summary": "Updated summary...",
    "categories": ["Category 1", "Category 4"]
}

Response Body:
{
    "id": 2,
    "title": "Updated Content Title",
    "body": "Updated content details...",
    "summary": "Updated summary...",
    "document": "/media/documents/new_content.pdf",
    "user_type": 1,
    "categories": ["Category 1", "Category 4"]
}


7. Delete Author's Content API
Endpoint: /delete_author_content/
Method: DELETE

Response Body:
{
    "message": "Content deleted successfully"
}


---------------------------For Admins side---------------------- 

8. View Admin's Contents API
Endpoint: /view_all_contents/
Method: GET

Response Body:
[
    {
        "id": 1,
        "title": "Sample Content",
        "body": "Lorem ipsum...",
        "summary": "A brief summary...",
        "document": "/media/documents/sample_content.pdf",
        "user_type": 1,
        "categories": ["Category 1", "Category 2"]
    },
    {
        "id": 2,
        "title": "New Content",
        "body": "Content details...",
        "summary": "A brief summary...",
        "document": "/media/documents/new_content.pdf",
        "user_type": 1,
        "categories": ["Category 1", "Category 3"]
    },
    // Other contents...
]


9. Edit Admin's Content API
Endpoint: /edit_content/
Method: PUT or PATCH

Request Body:
{
    "title": "Updated Content Title",
    "body": "Updated content details...",
    "summary": "Updated summary...",
    "categories": ["Category 1", "Category 4"]
}

Response Body:
{
    "id": 2,
    "title": "Updated Content Title",
    "body": "Updated content details...",
    "summary": "Updated summary...",
    "document": "/media/documents/new_content.pdf",
    "user_type": 1,
    "categories": ["Category 1", "Category 4"]
}

10. Delete Admin's Content API
Endpoint: /delete_content/
Method: DELETE

Response Body:
{
    "message": "Content deleted successfully"
}


-------------------------------------Thank you-------------------------------------------------















