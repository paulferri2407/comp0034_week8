"""Flask config class."""
from pathlib import Path


class Config(object):
    '''
    This is a teaching instruction and not a docstring for the function!
    Try the following code in a Python console to generate your own secret key and then past it below where it
    currently says 'generate_a_secret_key'. This uses secrets: https://docs.python.org/3/library/secrets.html

    import secrets
    print(secrets.token_urlsafe(16))
    '''
    SECRET_KEY = 'generate_a_secret_key'
    WTF_CSRF_SECRET_KEY = "crFAuXFCPKbKWw8JAKfnSA"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(Path(__file__).parent.joinpath('my_example.sqlite'))
    TESTING = False
    UPLOADED_PHOTOS_DEST = Path(__file__).parent.joinpath("static/img")


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_ECHO = True
