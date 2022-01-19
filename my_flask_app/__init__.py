from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect


csrf = CSRFProtect()
db = SQLAlchemy()


def create_app(config_class_name):
    """
    Initialise the Flask application.
    :type config_class_name: Specifies the configuration class
    :rtype: Returns a configured Flask object
    """
    app = Flask(__name__)
    app.config.from_object(config_class_name)
    csrf.init_app(app)
    db.init_app(app)

    with app.app_context():
        from my_flask_app.models import User
        db.create_all()

    from my_flask_app.main.routes import main_bp
    app.register_blueprint(main_bp)

    from my_flask_app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    return app
