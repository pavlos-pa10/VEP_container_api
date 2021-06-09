from flask import Flask, render_template
import os, pwd

def create_app():
    # Create the Flask application
    app = Flask(__name__)
    
    # Configure the Flask application
    config_type = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
    app.config.from_object(config_type)
    register_blueprints(app)
    return app


def register_blueprints(app):
    # Import the blueprints
    from project.views import views_blueprint
    

    # register each Blueprint with the Flask application instance (app)
    app.register_blueprint(views_blueprint)
