from flask import request, session
from flask_restful import Resource
from models import db, User


class Signup(Resource):
    def post(self):
        data = request.get_json()
        
        # Check for existing user.
        if User.query.filter_by(username=data['username']).first():
            return {'error': 'User name is already taken.'}, 409
            
        user = User(
            username=data['username'],
            email=data['email']
        )
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        return user.to_dict(), 201
    
    
    
    
class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data['password']).first()
        
        if user and user.check_password(data['password']):
            session['user_id'] = user.id
            return user.to_dict(
                rules=(
                    '-password_hash'
                    )), 200
        
        return {'error': 'Invalid credentials'}, 401
    
    
    
    
class Logout(Resource):
    def delete(self):
        session.pop('user_id', None)
        return {}, 204
    
    
    
class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        users_data = [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
            for user in users
        ]
        return users_data, 200
    
    
class UserById(Resource):
    def get(self, id):
        user = User.query.get(id)
        if not user:
            return {'error': 'User not found.'}, 404
        
        status_filter = request.args.get('status')
        
        if status_filter:
            filtered_assignments = [
                a for a in user.assignments if a.status.lower() == status_filter.lower()
            ]
        else:
            filtered_assignments = user.assignments
        
        assignments_data = [
            {
                "assignment_id": assignment.id,
                "chore_title": assignment.chore.title if assignment.chore else None,
                "assigned_date": assignment.assigned_date.isoformat() if assignment.assigned_date else None,
                "due_date": assignment.due_date.isoformat() if assignment.due_date else None,
                "status": assignment.status
            }
            for assignment in filtered_assignments
        ]
        
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "assignments": assignments_data
        }
        
        return user_data, 200
      
            
            
    
    
class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            if user:
                return user.to_dict(), 200
            return {'error': "Not logged in"}, 401
        
        
            
        