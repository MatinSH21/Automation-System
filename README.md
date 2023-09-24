# Automation System

The Automation System is an API-based automation built on the Django framework, and it designed to make organization's 
internal operations easier and more systematic.

## Table of Contents
- [About](#about)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)

## About

In this project, you can create roles based on employees' job descriptions and restrict their access to specific parts 
of the project. You can also assign tasks to employees.

## Features

- Task Management: Create, assign, update, delete tasks for employees
- Employee Management: Manage employee roles, permissions, and profiles
- Authentication and Authorization: Utilizes a Token-based system, where employees' access is determined by their 
roles

## Getting Started

Follow step-by-step instructions for setting up the project locally.

### Prerequisites
- Python 3.11.1
- Django 3.2

### Installation 

1. Clone the repository:
   ```sh
   git clone https://github.com/MatinSH21/Automation-System.git
2. Navigate into the cloned directory:
    ```sh
   cd [project-location]
3. Create a virtual environment (optional but recommended):
    ```sh
   python -m venv venv
4. Activate the virtual environment (If you followed step #3):
    ```sh
   venv/Scripts/activate
5. Install project dependencies: 
    ```sh
   pip install -r requirements.txt
6. Database migration:
    ```sh
   python manage.py migrate
7. Create superuser:
    ```sh
   python manage.py createsuperuser
8. Run the Django development server:
    ```sh
   python manage.py runserver
9. Check API documentation for more information:
    http://127.0.0.1:8000/swagger/
