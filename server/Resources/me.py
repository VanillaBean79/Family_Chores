# resources/me.py
from flask_restful import Resource
from flask import request

class Me(Resource):
    def get(self):
        user = getattr(request, "current_user", None)
        if not user:
            return {"error": "Unauthorized"}, 401

        # Include assignments with chore info
        user_dict = user.to_dict()
        user_dict['assignments'] = [
            {
                "id": a.id,
                "status": a.status,
                "chore": {
                    "id": a.chore.id,
                    "title": a.chore.title,
                    "description": a.chore.description
                }
            }
            for a in user.assignments
        ]
        return user_dict, 200
