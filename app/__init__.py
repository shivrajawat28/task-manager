from flask import Flask
from flask_sqlalchemy import SQLAlchemy  

# creating a global db object
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # configuration
    app.config['SECRET_KEY'] = 'MY-SECRET-KEY'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # connect database
    db.init_app(app)

    # import and register blueprints
    from app.routes.auth import auth_bp
    from app.routes.tasks import task_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp, url_prefix="/tasks")

    return app
