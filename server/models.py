from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates, relationship
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)

    assignments = relationship('Assignment', back_populates='user', cascade='all, delete-orphan')

    serialize_rules = (
        '-password_hash',
        '-assignments.user',
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @validates('username')
    def validate_username(self, key, value):
        if not value or not value.strip():
            raise ValueError("Username is required.")
        return value

    @validates('email')
    def validate_email(self, key, value):
        if not value or '@' not in value:
            raise ValueError("Valid email required.")
        existing_user = User.query.filter_by(email=value).first()
        if existing_user:
            raise ValueError("Email already in use.")
        return value


class Assignment(db.Model, SerializerMixin):
    __tablename__ = 'assignments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    chore_id = db.Column(db.Integer, db.ForeignKey('chores.id'), nullable=False)
    assigned_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='pending')

    user = relationship('User', back_populates='assignments')
    chore = relationship('Chore', back_populates='assignments')

    serialize_rules = (
        '-user.assignments',
        '-chore.assignments',
    )


class Chore(db.Model, SerializerMixin):
    __tablename__ = 'chores'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    frequency = db.Column(db.String(20))

    assignments = relationship('Assignment', back_populates='chore', cascade='all, delete-orphan')

    serialize_rules = (
        '-assignments.chore',
    )

    @validates('title')
    def validate_title(self, key, value):
        if not value or not value.strip():
            raise ValueError('Title cannot be blank.')
        return value
