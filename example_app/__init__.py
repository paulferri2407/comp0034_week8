from pathlib import Path

import pandas as pd
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()
db = SQLAlchemy()
login_manager = LoginManager()
photos = UploadSet('photos', IMAGES)


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
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    configure_uploads(app, photos)

    with app.app_context():
        from example_app.models import User, Profile, Region
        db.create_all()
        add_noc_data(db)

        # Import Paralympics Dash application
        from .paralympic_app.paralympic_app import create_dash
        app = create_dash(app)

    from example_app.main.routes import main_bp
    app.register_blueprint(main_bp)

    from example_app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    return app


def add_noc_data(db_name):
    """ Adds the list of countries to the NOCRegion table to the database.
    :param db_name: the SQLite database initialised for the Flask app
    :type db_name: SQLAlchemy object
    """
    filename = Path(__file__).parent.joinpath('paralympic_app', 'data', 'noc_regions.csv')
    df = pd.read_csv(filename, usecols=['region'])
    df.dropna(axis=0, inplace=True)
    df.drop_duplicates(subset=['region'], keep='first', inplace=True)
    df.reset_index(drop=True, inplace=True)
    df['id'] = df.index
    df.to_sql(name='region', con=db.engine, if_exists='replace', index=False)
