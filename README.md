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
