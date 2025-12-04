from flask_restful import Resource
from flask import request, session
from models import User, db


class AddChild(Resource):
    """Allows a parent to add a child account."""
    def post(self):
        parent_id = session.get('user_id')
        if not parent_id:
            return {'error': 'Unauthorized'}, 401

        data = request.get_json()
        if not data.get('username') or not data.get('password') or not data.get('email'):
            return {'error': 'Missing required fields'}, 400

        # Create child user linked to parent
        child = User(
            username=data['username'],
            email=data['email'],
            role='child',
            parent_id=parent_id
        )
        child.set_password(data['password'])

        db.session.add(child)
        db.session.commit()

        return {
                "id": child.id,
                "username": child.username,
                "role": child.role
                }, 201


class Children(Resource):
    def get(self):
        parent_id = session.get('user_id')  # make sure session key matches login
        if not parent_id:
            return {"error": "Unauthorized"}, 401

        parent = User.query.get(parent_id)
        if not parent or parent.role != "parent":
            return {"error": "Unauthorized"}, 401

        children = User.query.filter_by(parent_id=parent.id, role="child").all()
        
        children_data = [
            {
                "id": child.id,
                "username": child.username,         # 🔹 include username
                "role": child.role,
                "chore_count": len(child.assignments)  # 🔹 include chore_count
            }
            for child in children
        ]
        
        return children_data, 200
    
    
    
class DeleteChild(Resource):
    def delete(self, child_id):
        parent_id = session.get("user_id")
        if not parent_id:
            return{"error": "Unauthorized."}, 401
        
        child = User.query.get(child_id)
        if not child or child.parent_id != parent_id:
            return {"error": "Child not found or unauthorized"}, 404
        
        db.session.delete(child)
        db.session.commit()
        return {"message": f"Child {child.username} deleted successfully."}, 200
