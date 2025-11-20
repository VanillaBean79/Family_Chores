from flask import request, session
from flask_restful import Resource
from models import db, User, Assignment, Chore 
from sqlalchemy.orm import joinedload


class Signup(Resource):
    def post(self):
        data = request.get_json()
        
        # Check for existing user.
        if User.query.filter_by(username=data['username']).first():
            return {'error': 'User name is already taken.'}, 409
        
            
        user = User(
            username=data['username'],
            email=data['email'],
            role='parent'
        )
        
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        
        session['parent_id'] = user.id
        
        return user.to_dict(), 201
    
    
    
    
class Login(Resource):
    def post(self):
        data = request.get_json()
        
        # Find user by username regardless of role
        user = User.query.filter_by(username=data["username"]).first()
        
        if not user or not user.check_password(data["password"]):
            return {"error": "Invalid username or password"}, 401
        
        # Store generic session key for all users
        session["user_id"] = user.id
        
        # Return role so frontend knows where to redirect
        return {
            "id": user.id,
            "username": user.username,
            "role": user.role
        }, 200

    
    
    
    
class Logout(Resource):
    def delete(self):
        session.pop('parent_id', None)
        return {'message': 'Logged out'}, 204
    
    
class ChildLogin(Resource):
    def post(self):
        data = request.get_json()
        child = User.query.filter_by(username=data['username'], role='child').first()
        if not child or not child.check_password(data['password']):
            return {'error': 'Invalid credentials'}, 401

        session['child_id'] = child.id
        return child.to_dict(), 200
    
    
    
    
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
        if 'user_id' in session:
            print("🧩 Session contents:", dict(session))  # Debug line
            # ✅ Use joinedload to eager load assignments + chore in one query
            user = (
                db.session.query(User)
                .options(joinedload(User.assignments).joinedload(Assignment.chore))
                .get(session['user_id'])
            )

            if not user:
                return {"error": "User not found"}, 404

            # Build structured assignment data
            assignments_data = []
            for assignment in user.assignments:
                assignments_data.append({
                    "id": assignment.id,
                    "status": assignment.status,
                    "assigned_date": assignment.assigned_date.isoformat() if assignment.assigned_date else None,
                    "due_date": assignment.due_date.isoformat() if assignment.due_date else None,
                    "chore": {
                        "id": assignment.chore.id if assignment.chore else None,
                        "title": assignment.chore.title if assignment.chore else None,
                        "description": assignment.chore.description if assignment.chore else None,
                    } if assignment.chore else None
                })

            return {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "assignments": assignments_data
            }, 200

        return {"error": "Not logged in"}, 401
    
    
# class AddChild(Resource):
#     def post(self):
#         #Ensure parent is logged in
#         parent_id = session.get("user_id")
#         if not parent_id:
#             return{"error": "Only parents can add children"}
        
#         parent = User.query.get(parent_id)
#         if parent.role != "parent":
#             return {"error": "Only parents can add children"}
        
#         # Get Child data from request
        
#         data = request.get_json()
#         username = data.get("username")
#         email = data.get("email")
#         password = data.get("password")
        
        
#         #check fi username or email is already taken
#         if User.query.filter_by(username=username).first():
#             return{"error": "Username is already taken"}, 409
#         if User.query.filter_by(email=email).first():
#             return {"error": "Email is already taken"}, 409
        
#         #Create child user
#         child = User(username=username, email=email, role=child)
#         child.set_password(password)
        
        
#         db.session.add(child)
#         db.session.commit()
        
#         return child.to_dict(), 201
        
        
            
        