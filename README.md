# BookMate: Student Book Rental System

**BookMate** is a web application designed for students to rent books for free for the first month. After that, a rental fee is applied based on the book's page count. The application utilizes the [ISBNDB API](https://isbndb.com/) to fetch book details automatically, streamlining the rental process.

---

## Features

- **Free Rentals**: Students can rent books for one month without any charges.
- **Rental Fees**: After the initial month, fees are calculated based on the book's page count, with a rate of $1 per 100 pages.
- **Admin Features**:
  - CRUD of Book and Rentals(soft delete is not implemented).
  - View a student's dashboard with total pending fees and rental history.
- **ISBNDB API Integration**: Fetches book details (title, author, page count) based on the book's title.
- **Django Admin Interface**: Provides easy management of users, books, rentals, and student dashboards.
- **Return Flag**: Automatically handles when book return date is provided.
- **Book Availability**: Ensures that only available books are rented in admin panel.

---

## Technology Stack

- **Backend**: Django, Django REST Framework (DRF)
- **Database**: SQLite (default)
- **External API**: ISBNDB API
- **Authentication**: Django's built-in authentication system

---

## Installation

### Prerequisites

Ensure the following tools are installed on your machine:

- Python 3.13
- pip (Python package installer)
- Virtual environment tools (`venv` or `virtualenv`)

### Setup Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/RonakDelvadiya/bookmate.git
   cd bookmate
   ```
   The repository also includes the database.

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv env
   source env/bin/activate   # For Windows: env\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a superuser**:
   Alternatively, you can use the default credentials: `admin/admin`
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

6. **Set up environment variables**:
   - Copy the environment variables from the [project's settings](https://github.com/RonakDelvadiya/bookmate/settings/variables/actions).
   - Create a `.env` file and add the environment variables according to the project structure.

7. **Access the application**:
   Open your browser and navigate to `http://127.0.0.1:8000/`
  
   - The **Admin Panel** can be accessed at `http://127.0.0.1:8000/admin/`.
   - The **Student Dashboard** is available at `http://127.0.0.1:8000/rentals/rental/student_dashboard/`.

---

## API Endpoints

### Books API

| Method | Endpoint                 | Description                              |
|--------|--------------------------|------------------------------------------|
| GET    | `/api/books/book-list/`   | List all books                           |

CRUD operations for books can also be performed via the Admin Panel at: `http://127.0.0.1:8000/admin/books/book/`

### Rentals API

| Method | Endpoint                        | Description                                              |
|--------|----------------------------------|----------------------------------------------------------|
| GET    | `/api/rentals/rental-list-create/`| List all rentals                                         |
| POST   | `/api/rentals/rental-list-create/`| Create a new rental                                      |
| GET    | `/api/rentals/rental-action/{id}/`| Retrieve a specific rental by ID                         |
| PUT    | `/api/rentals/rental-action/{id}/`| Extend a rental (automatically computes fees if needed)  |
| DELETE | `/api/rentals/rental-action/{id}/`| Delete a specific rental                                 |

CRUD operations for rentals can also be performed via the Admin Panel at: `http://127.0.0.1:8000/admin/rentals/rental/`

---

## Usage

### Adding a Book (via Admin Panel)

Admins can add books directly from the Admin Panel. When adding a book, the system will automatically fetch its details (title, author, page count) from the ISBNDB API based on the provided title.

### Renting a Book

Admins can create, update, and manage rentals via the Admin Panel or API. Key rental operations include:

1. After one month, extending a rental will automatically apply a fee based on the book's page count. 
2. **The rental period will be rounded up to the nearest whole month. For example, 1.2 or 1.8 months will be considered as 2 months.**
3. All rental-related validation is managed at the model level:
   - Return dates cannot be earlier than the rental date or later than the current date.
   - The system manages book availability and ensures that only available books are rented.
   - The book return status is automatically updated when the return date is provided.
   - Only staff members (is_staff=True) will be avialble as created_by or modified_by in rentals.

---

## Admin Panel

The admin interface provides full control over the management of books, rentals, and users.

To access the admin panel:
1. Navigate to `http://127.0.0.1:8000/admin/`.
2. Log in using the superuser credentials or default credentials.
3. Admins can manage books and rentals, with validations and checks implemented in the models and admin configurations for the respective apps (Books, Rentals).

---

## Project Structure

```
bookmate/
│
├── apps/
│   ├── books/                    # Manages book data
│   ├── rentals/                  # Manages rental data
│   ├── utils/                    # Utility functions
│
├── bookmate/                     # Django project 
│   ├── urls.py                   # Project URL routing
│   └── settings.py               # Project configuration
│
├── templates/                    # HTML templates
│   ├── admin/
│       ├── rental_changelist.html    # Rental changelist template
│       └── student_dashboard.html    # Student dashboard template
│
├── db.sqlite3                    # Default SQLite database
├── requirements.txt              # Python dependencies
├── .env                          # Environment variables(needs to be create during setup)
├── manage.py                     # Django management script
└── README.md                     # Project documentation (this file)

```
