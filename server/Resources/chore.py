from flask_restful import Resource
from flask import request
from models import db, Chore

class ChoreList(Resource):
    def get(self):
        chores = Chore.query.all()
        return [chore.to_dict() for chore in chores], 200

    def post(self):
        data = request.get_json()
        if not data.get("title"):
            return {"error": "Title is required"}, 400

        chore = Chore(title=data["title"], description=data.get("description"))
        db.session.add(chore)
        db.session.commit()
        return chore.to_dict(), 201
    
class ChoreById(Resource):
    def patch(self, chore_id):
        chore = Chore.query.get(chore_id)
        if not chore:
            return {"error": "Chore not found"}, 404

        data = request.get_json()
        if "title" in data:
            chore.title = data["title"]
        if "description" in data:
            chore.description = data["description"]
        if "due_date" in data:
            from datetime import datetime
            try:
                chore.due_date = datetime.fromisoformat(data["due_date"])
            except ValueError:
                return {"error": "Invalid due_date format. Use ISO format like '2025-12-30T18:00:00'"}, 400

        db.session.commit()
        return chore.to_dict(), 200

    def delete(self, chore_id):
        chore = Chore.query.get(chore_id)
        if not chore:
            return {"error": "Chore not found"}, 404
        
        db.session.delete(chore)
        db.session.commit()
        return {"message": "Chore deleted"}, 200
