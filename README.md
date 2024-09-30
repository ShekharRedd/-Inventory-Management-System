            Inventory Management System API Documentation

## Overview  

This project implements a backend API for an Inventory Management System using Django Rest Framework (DRF). The system provides secure endpoints for CRUD operations on inventory items, with JWT-based authentication for access control. Redis is used to cache frequently accessed items to improve performance, and PostgreSQL is used as the database. Comprehensive logging is integrated for monitoring and debugging, and unit tests ensure the API's reliability.  


## Table of Contents

1. [Project Setup]  
2. [Authentication]  
3. [API Endpoints]  
   - [Create Item]  
   - [Read Item]  
   - [Update Item]    
   - [Delete Item]  
4. [Redis Caching]  
5. [Logging]  
6. [Unit Testing]  
7. [Technologies Used]  
8. [Contributing]  

## Project Setup

### Prerequisites

To run this project, ensure you have the following installed:

- Python 3.8+
- PostgreSQL (Mysql)
- Redis
- Pip (Python package installer)
- Django and Django Rest Framework


### Installation Steps

1. **Clone the Repository**:
   
   
   git clone <your-repository-url>
   cd <project-directory>
   

2. **Create and Activate a Virtual Environment**:

   
   python3 -m venv env
   source env/bin/activate  # For Windows: env\Scripts\activate
   

3. **Install Dependencies**:

   
   pip install -r requirements.txt
   

4. **Set Up PostgreSQL Database**:
   
   - Create a PostgreSQL database.
   - Update the database configuration in `settings.py`:
   
   python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your_db_name',
           'USER': 'your_db_user',
           'PASSWORD': 'your_db_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   

5. **Run Migrations**:

   
   python manage.py migrate
   

6. **Start the Redis Server**:

   
   redis-server
   

7. **Start the Django Server**:

   
   python manage.py runserver
   

8. **Create Superuser for Admin Access (optional)**:

   
   python manage.py createsuperuser



## Authentication (JWT)  

This API uses JSON Web Token (JWT) authentication. To access most endpoints, users need to provide a valid JWT token. You can register new users and obtain tokens as described below.  

### User Registration  

- **Endpoint**: `/register/`
- **Method**: `POST`
- **Request Body**: 
  json
  {
      "username": "your_username",
      "email": "your_email",
      "password": "your_password"
  }
 
###User Login and Token Generation

- **Endpoint**: `/login/`
- **Method**: `POST`
- **Request Body**:  
  json
  {
      "email": "your_email",
      "password": "your_password"
  }
  

- **Response**: 
  json
  {
      "refresh": "refresh_token_here",
      "access": "access_token_here"
  }
  

- Use the `access` token in the Authorization header for authenticated requests:
  http
  Authorization: Bearer <your_access_token>



## API Endpoints

### Create Item

- **Method**: `POST`
- **URL**: `/items/`
- **Request Body**: 
  json
  {
      "name": "item_name",
      "description": "item_description",
      "quantity": 10,
      "price": 50.00
  }
  
- **Response**:
  json
  {
      "id": 1,
      "name": "item_name",
      "description": "item_description",
      "quantity": 10,
      "price": 50.00
  }
  
- **Error Codes**:
  - `400`: Item already exists.

### Read Item

- **Method**: `GET`
- **URL**: `/items/{item_id}/`
- **Response**:
  json
  {
      "id": 1,
      "name": "item_name",
      "description": "item_description",
      "quantity": 10,
      "price": 50.00
  }
  
- **Error Codes**:
  - `404`: Item not found.

### Update Item

- **Method**: `PUT`
- **URL**: `/items/{item_id}/`
- **Request Body**:
  json
  {
      "name": "updated_item_name",
      "description": "updated_item_description",
      "quantity": 20,
      "price": 100.00
  }
  
- **Response**:
  json
  {
      "id": 1,
      "name": "updated_item_name",
      "description": "updated_item_description",
      "quantity": 20,
      "price": 100.00
  }
  
- **Error Codes**:
  - `404`: Item not found.

### Delete Item

- **Method**: `DELETE`
- **URL**: `/items/{item_id}/`
- **Response**: 
  json
  {
      "message": "Item deleted successfully."
  }
  
- **Error Codes**:
  - `404`: Item not found.


## Redis Caching

To improve performance, items are cached in Redis. When a user accesses an item for the first time, it is stored in the cache. Subsequent requests for the same item will retrieve the data from Redis instead of querying the database.

- Redis is automatically used in the `GET /items/{item_id}/` endpoint for cached data.


## Logging

The project integrates logging to track errors and API usage. Logs are stored in the `logs/app.log` file, where significant events are recorded, such as:

- API requests
- User login and registration
- Item CRUD operations
- Errors and exceptions

### Logging Configuration Example:
python
import logging
import os

log_dir = os.path.join(os.path.dirname(__file__), 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    filename=os.path.join(log_dir, 'app.log'),
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)



## Unit Testing

Unit tests are provided for all API endpoints, including both successful and error cases. To run the tests:


python manage.py test


Test cases cover:

- User registration and login
- JWT authentication
- Item CRUD operations
- Redis caching
- Error handling


## Technologies Used

- **Backend**: Django Rest Framework (DRF)
- **Database**: PostgreSQL
- **Caching**: Redis
- **Authentication**: JWT (JSON Web Token)
- **Logging**: Python's logging library



## Conclusion

This documentation provides a complete overview of the Inventory Management System, covering setup, API usage, authentication, caching, logging, and testing. Follow the steps mentioned to install, run, and test the project, and feel free to contribute.
