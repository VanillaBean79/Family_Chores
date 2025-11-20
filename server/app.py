import os
import tempfile
from flask import Flask, session, request
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_session import Session
from dotenv import load_dotenv

from config import DevelopmentConfig
from models import db
from resources.user import Signup, Login, Logout, CheckSession, UserListResource, UserById
from resources.chore import ChoreList
from resources.assignment import AssignmentList, AssignmentById 
from resources.child import AddChild, Children

load_dotenv()

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # ✅ Make sure session directory exists
    app.config["SESSION_FILE_DIR"] = os.path.join(tempfile.gettempdir(), "flask_session")
    os.makedirs(app.config["SESSION_FILE_DIR"], exist_ok=True)

    # ✅ Initialize extensions in the correct order
    db.init_app(app)
    migrate = Migrate(app, db)
    CORS(app, origins=["http://localhost:3000"], supports_credentials=True)
    Session(app)

    api = Api(app)

    @app.before_request
    def load_current_user():
        user_id = session.get('user_id')
        if user_id:
            from models import User
            request.current_user = User.query.get(user_id)
        else:
            request.current_user = None

    # API routes
    api.add_resource(Signup, '/signup')
    api.add_resource(Login, '/login')
    api.add_resource(Logout, '/logout')
    api.add_resource(CheckSession, '/me')
    api.add_resource(UserListResource, '/users')
    api.add_resource(UserById, '/users/<int:id>')
    api.add_resource(ChoreList, '/chores')
    api.add_resource(AssignmentList, '/assignments')
    api.add_resource(AssignmentById, '/assignments/<int:id>')
    # api.add_resource(AddChild, "/add-child")
    api.add_resource(AddChild, "/children/add")
    api.add_resource(Children, '/children/list')
    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(port=5555, debug=True)
