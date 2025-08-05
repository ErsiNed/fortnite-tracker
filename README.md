# Fortnite Spending Tracker 💸

A Django web application that helps you track your Fortnite V-Bucks purchases, earnings, and spending history.

---

## 🚀 Features

- Track real money transactions by category (V-Bucks, Crew Pack, Quest Pack, etc.)
- Automatically calculate and update V-Bucks balance
- View total V-Bucks earned, spent, and remaining
- Upload and display user avatars
- Profile and transaction management (CRUD)
- Clean, responsive UI using Bootstrap 5

---

## 🌐 API Capabilities

I've implemented complete REST capabilities as standalone endpoints. 
While the current web interface uses traditional Django templates, the API layer is fully functional 
and ready for future JavaScript or mobile integration.

**Available Endpoints**:
- `POST /api/token/` - Get JWT tokens (provide `username`/`password`)
- `GET /api/users/` - List all users (requires JWT)
- `GET /api/users/<id>/` - Get user details

---

## 🛠️ Technologies

- **Python 3.11+** & **Django 4.2**
- SQLite (default, can be swapped for PostgreSQL)
- Bootstrap 5
- HTML5 & CSS3

---

## ⚙️ Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/ErsiNed/fortnite-tracker.git
   cd fortnite-tracker
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate     # macOS/Linux
   .venv\Scripts\activate        # Windows
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations:**

   ```bash
   python manage.py migrate
   ```

5. **(Optional) Create a superuser:**

   ```bash
   python manage.py createsuperuser
   ```
6. **Set up Staff roles and permissions:**

   ```bash
   python manage.py setup_staff_role
   ```
   *This creates a 'Staff' group with the appropriate view and change permissions for:*
   - User and UserProfile models
   - Vbucks-related models (RealMoneyTransaction, VbucksEarning, VbucksSpending, Refund)

7. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

8. **Open in your browser:**

   ```
   http://127.0.0.1:8000
   ```

## ⚠️ Disclaimer

This project is for educational purposes only.  
It is **not affiliated with Epic Games or Fortnite** in any way.

---
