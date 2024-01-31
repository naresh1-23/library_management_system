Library Management System
Overview

Setup Instructions

Installation
Clone the repository:

run below command in terminal

git clone https://github.com/your-username/library-management-system.git


cd library-management-system

Create a virtual environment and activate it:


python3 -m venv env


source env/bin/activate   # On Windows: venv\Scripts\activate

Install dependencies:


pip install -r requirement.txt


Apply database migrations:

python3 manage.py makemigrations


python3 manage.py migrate


Create a superuser for admin access:


python3 manage.py createsuperuser
Follow the prompts to create a superuser account.

Run the development server:


python3 manage.py runserver


Access the admin interface at http://localhost:8000/admin/ and log in with the superuser credentials.

API is accessible at http://localhost:8000/api/

API Documentation
User Endpoints
Create user

Endpoint: POST /api/users/


Request Body: JSON with full_name, email,password and membership_date


Get Users List

Endpoint: GET /api/users/

GET Single user using user id

Endpoint: GET /api/user_detail/{user_id}/

Update user

Endpoint: PUT /api/user_detail/{user_id}/


Request Body: Same as create user

Delete user

Endpoint: DELETE /api/user_detail/{user_id}/


Books endpoint

Add Book

Endpoint: POST /api/books_list/



Request Body: JSON with title, isbn, publishedDate and genre

get all books

Endpoint: GET /api/books_list/

book detail endpoint

Add bookdetail

Endpoint: POST /api/booksdetail_list/



Request Body: JSON with book_id, number_of_page, publisher, and language

get all books detail

Endpoint: GET /api/booksdetail_list/

get single book detail by book id

Endpoint: GET /api/bookdetail/{book_id}/

update book detail by book id

Endpoint: PUT /api/bookdetail/{book_id}/


Request Body: Same as add book detail

delete book detail by book id 

Endpoint: DELETE /api/bookdetail/{book_id}/

Book borrower
Add book borrower

Endpoint: POST /api/book_borrowers/


Request Body: JSON with user_id, book_id, borrowed_date and returned_date where returned_date is not necessary if no data.

get all list of borrowers

Endpoint: GET /api/book_borrowers/

get single data of borrower by the id of user

Endpoint: GET /api/borrower/{user_id}/

update data of borrower by the id of user

Endpoint: PUT /api/borrower/{user_id}/


Request Body: Same as add book borrower

delete data of the borrower by the id of user

Endpoint: DELETE /api/borrower/{user_id}/

Endpoint for login

Endpoint: POST /api/login/


Request Body: JSON with email and password


Additional Notes
Before using api. You can first login using login api with superuser account. So that you can access the api which are not accessible for normal user.

I have made changes in adding user where admin should add password when creating user. I haven't added the functionality or api to add the user itself or register by user own. Only admin can add user.

User authentication is implemented using token system. Token is generated using django rest framework simple jwt.

This system assumes a one-to-one relationship between Book and BookDetail, and a one-to-many relationship between User and BorrowedBooks.

I have added login api to login the user. After logging in using the authorized data api will provide a token. Use that token in bearer token in authentication of postman. 

Also I have added permissions to only admin i.e superuser to add, delete and update the books detail , book borrower, or users. Also, only admin can see the list of user. Admin is created by command 
python3 manage.py createsuperuser.


