from flask_restful import Resource
from flask import request, session
from models import User, db


class AddChild(Resource):
    """Allows a parent to add a child account."""
    def post(self):
        parent_id = session.get('parent_id')
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
    """Returns all children belonging to the logged-in parent."""
    def get(self):
        parent_id = session.get('parent_id')
        if not parent_id:
            return {"error": "Unauthorized"}, 401

        parent = User.query.get(parent_id)
        if not parent or parent.role != "parent":
            return {"error": "Unauthorized"}, 401

        children = User.query.filter_by(parent_id=parent.id, role="child").all()
        
        children_data = [
            {
                "id": child.id,
                "username": child.username,
                "role": child.role
            }
            for child in children
        ]
        
        return children_data, 200
