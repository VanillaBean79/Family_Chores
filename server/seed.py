# seed.py
from app import create_app
from models import db, User, Chore, Assignment
from datetime import datetime, timedelta

app = create_app()

with app.app_context():
    # Clear the existing data
    print("Clearing old data...")
    Assignment.query.delete()
    Chore.query.delete()
    User.query.delete()
    db.session.commit()

    # Create users
    print("Creating users...")
    user1 = User(username="alice", email="alice@example.com")
    user1.set_password("password123")

    user2 = User(username="bob", email="bob@example.com")
    user2.set_password("securepass")

    db.session.add_all([user1, user2])
    db.session.commit()

    # Create chores
    print("Creating chores...")
    chore1 = Chore(title="Wash Dishes", description="Clean all dishes.", frequency="daily")
    chore2 = Chore(title="Vacuum", description="Vacuum all rooms.", frequency="weekly")
    chore3 = Chore(title="Take Out Trash", description="Empty all trash bins.", frequency="daily")

    db.session.add_all([chore1, chore2, chore3])
    db.session.commit()

    # Create assignments
    print("Creating assignments...")
    assignment1 = Assignment(
        user_id=user1.id,
        chore_id=chore1.id,
        assigned_date=datetime.utcnow(),
        due_date=datetime.utcnow() + timedelta(days=1),
        status="pending"
    )

    assignment2 = Assignment(
        user_id=user2.id,
        chore_id=chore2.id,
        assigned_date=datetime.utcnow(),
        due_date=datetime.utcnow() + timedelta(days=2),
        status="completed"
    )

    assignment3 = Assignment(
        user_id=user1.id,
        chore_id=chore3.id,
        assigned_date=datetime.utcnow(),
        due_date=datetime.utcnow() + timedelta(days=3),
        status="in progress"
    )

    db.session.add_all([assignment1, assignment2, assignment3])
    db.session.commit()

    print("✅ Database seeded successfully!")
