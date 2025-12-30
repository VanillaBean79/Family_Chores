from flask_restful import Resource
from flask import session
from models import User

class Me(Resource):
    def get(self):
        user_id = session.get("user_id")

        if not user_id:
            return {"error": "Unauthorized"}, 401

        user = User.query.get(user_id)

        if not user:
            return {"error": "User not found"}, 404

        return user.to_dict(), 200
