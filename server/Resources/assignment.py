from flask_restful import Resource
from models import db, Assignment, User, Chore 
from flask import request
from datetime import datetime


class AssignmentList(Resource):
    def get(self):
        assignments = Assignment.query.all()
        return [assignment.to_dict() for assignment in assignments]
    
    def post(self):
        data = request.get_json()

        # validate required fields
        user_id = data.get('user_id')
        chore_id = data.get('chore_id')

        if not user_id or not chore_id:
            return {"error": "user_id and chore_id are required"}, 400
        
        due_date_str = data.get('due_date')
        due_date = None
        if due_date_str:
            try:
                due_date = datetime.fromisoformat(due_date_str)
            except ValueError:
                return {"error": "Invalid date format. Use ISO format like '2025-09-30T18:00:00"}, 400

        # optionally validate that User and Chore exist
        user = User.query.get(user_id)
        chore = Chore.query.get(chore_id)
        if not user or not chore:
            return {"error": "User or Chore not found"}, 404

        assignment = Assignment(
            user_id=user_id,
            chore_id=chore_id,
            due_date=due_date,   # depends on your schema
            status=data.get('status', 'assigned')
        )

        db.session.add(assignment)
        db.session.commit()

        return assignment.to_dict(), 201
            
        
    
    
class AssignmentById(Resource):
    def get(self, id):
        assignment = Assignment.query.get(id)
        
        if not assignment:
            return {'error': 'Assignment not found'}, 404
        
        return assignment.to_dict(), 200
    
    
    def patch(self, id):
        assignment = Assignment.query.get(id)
        if not assignment:
            return {"error": "Assignment not found"}, 404

        data = request.get_json()

        # handle due_date separately because it needs parsing
        if "due_date" in data:
            try:
                assignment.due_date = datetime.fromisoformat(data["due_date"])
            except ValueError:
                return {"error": "Invalid date format. Use ISO format like '2025-09-30T18:00:00'"}, 400

        # simple fields that don’t need parsing
        if "status" in data:
            assignment.status = data["status"]

        db.session.commit()

        return assignment.to_dict(), 200
    
    
    def delete(self, id):
        assignment = Assignment.query.get(id)
        if not assignment:
            return {'error': 'Assignment not found'}, 404
        
        db.session.delete(assignment)
        db.session.commit()
        
        return {'message': f"Assignment {id} deleted successfully"}, 200
        

                
                
        
        
        
        
    
    
    