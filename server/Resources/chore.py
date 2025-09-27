from flask_restful import Resource
from flask import Response
import json
from models import Chore

class ChoreList(Resource):
    def get(self):
        chores = Chore.query.all()
        chores_dict = [chore.to_dict() for chore in chores]
        
        pretty_json = json.dumps(chores_dict, indent=2)
        return Response(pretty_json, mimetype='application/json')  # no , 200 here

