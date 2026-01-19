# Family Chores

A full-stack web application to help families manage household chores. Parents can add children, create chores, assign chores to children with due dates, and monitor completion. Children can view their assigned chores, mark them as completed, and receive encouraging feedback.

---

## Table of Contents

- [Demo](#demo)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup](#setup)
- [Usage](#usage)
- [Folder Structure](#folder-structure)
- [Contributing](#contributing)
- [License](#license)

---

## Demo

Add a screenshot or GIF here:


---

## Features

### Parent Dashboard
- Add, edit, and delete children.
- Create and manage chores.
- Assign chores to children with due dates.
- Receive notifications when a child completes a chore (messages in bright green).
- Track the status of each child’s chores.

### Child Dashboard
- View assigned chores.
- See chore descriptions and due dates.
- Mark chores as completed.
- Confetti animation and encouraging messages upon completion.

---

## Tech Stack

**Frontend:**
- React
- JavaScript (ES6+)
- CSS (modular components)
- React Confetti for completion animations

**Backend:**
- Python
- Flask
- Flask-RESTful
- SQLAlchemy ORM
- Flask-Migrate
- Flask-Session
- Flask-CORS

**Database:**
- SQLite (development)
- Can be switched to PostgreSQL or MySQL in production

---

## Setup

### Backend

1. Clone the repository:

```bash
git clone https://github.com/your-username/family-chores.git
cd family-chores
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt
FLASK_ENV=development
SECRET_KEY=your_secret_key
flask db init
flask db migrate
flask db upgrade
python app.py


cd client
npm install
npm start



family-chores/
├── client/                  # React frontend
│   ├── src/
│   │   ├── components/      # Reusable components (AddChildForm, AssignChore, etc.)
│   │   ├── pages/           # Dashboard pages
│   │   ├── styles/          # CSS files
│   │   └── App.js
├── migrations/              # Flask-Migrate migration files
├── resources/               # Flask-RESTful resources
├── models.py                # SQLAlchemy models
├── app.py                   # Flask app factory
├── config.py                # Configuration
├── requirements.txt         # Python dependencies
└── README.md
