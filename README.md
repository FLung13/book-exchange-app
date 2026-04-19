# Book Exchange App (Django)

A web-based book management and exchange platform built with Django, allowing users to browse, add, and manage books through a structured backend system.

This project demonstrates full-stack web development fundamentals, including backend logic, templating, and database-driven applications.

---

## Overview

The Book Exchange App is a Django-based web application that simulates a simple platform for managing and sharing books. It provides functionality for creating, viewing, and organizing book records using a relational database.

The project focuses on backend development and server-side rendering using Django’s built-in tools.

---

## Key Features

- Add and manage book records  
- View a list of available books  
- Server-rendered HTML using Django templates  
- Form handling and validation  
- Admin panel for data management  
- Organized app structure using Django best practices  

---

## Tech Stack

- **Backend:** Django (Python)  
- **Frontend:** HTML, CSS (Django Templates)  
- **Database:** SQLite  
- **Other:** Django ORM, Forms, Admin Interface  

---

## Project Structure
```
├── manage.py
├── bookEx/
│ ├── settings.py
│ ├── urls.py
│ ├── templates/
│ └── static/
└── bookMng/
├── models.py
├── views.py
├── forms.py
├── urls.py
├── admin.py
└── migrations/
```

---

## How It Works

The application follows Django’s standard architecture:

1. **Models** define the database structure for books  
2. **Views** handle logic and process requests  
3. **Templates** render dynamic HTML pages  
4. **Forms** manage user input and validation  
5. **URLs** route requests to the appropriate views  

---

## Getting Started

### Prerequisites

- Python 3.x
- pip

### Installation

```bash
git clone https://github.com/FLung13/book-exchange-app.git
cd book-exchange-app
```
Install dependencies:
```bash
pip install django widget-tweaks
```
Run migrations:
```bash
python manage.py migrate
```
Start the server:
```bash
python manage.py runserver
```
Then open:
```
http://127.0.0.1:8000/
```

### Environment Variables

Create a .env file in the project root:
```
SECRET_KEY=your-secret-key
```
This file is not included in the repository for security reasons.

### Admin Panel

To access the Django admin panel:
```bash
python manage.py createsuperuser
```
Then visit:
```
http://127.0.0.1:8000/admin/
```

## Limitations
  - No user authentication system for book ownership
  - No real-time updates or API layer
  - Basic UI (focus is on backend functionality)

## Future Improvements
  - Add user authentication and accounts
  - Implement book exchange requests between users
  - Improve UI/UX design
  - Add search and filtering functionality
  - Convert to REST API with Django REST Framework

## What This Project Demonstrates
  - Understanding of Django architecture (models, views, templates)
  - Experience with relational databases and ORM
  - Ability to build structured web applications
  - Backend-focused development with server-side rendering

## Author

Fredy Lung\
Software Developer

### Portfolio

This project is part of my software engineering portfolio.
Explore more projects here:

👉 https://fredylung.vercel.app/
