from pathlib import Path

import pandas as pd
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
        add_noc_data(db)

    from my_flask_app.main.routes import main_bp
    app.register_blueprint(main_bp)

    from my_flask_app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    return app


def add_noc_data(db_name):
    """ Adds the list of countries to the NOCRegion table to the database.
    :param db_name: the SQLite database initialised for the Flask app
    :type db_name: SQLAlchemy object
    """
    filename = Path(__file__).parent.parent.joinpath('paralympic_app', 'data', 'noc_regions.csv')
    df = pd.read_csv(filename, usecols=['region'])
    df.dropna(axis=0, inplace=True)
    df.drop_duplicates(subset=['region'], keep='first', inplace=True)
    df.reset_index(drop=True, inplace=True)
    df['id'] = df.index
    df.to_sql(name='region', con=db.engine, if_exists='replace', index=False)