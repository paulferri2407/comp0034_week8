# Using Flask-Login

In this activity you will:

1. Configure the application to use Flask-Login
2. Add the required helper functions
3. Add the routes for login and logout
4. Add login/logout to the navbar
5. Require a user to be logged in to access the community pages




Create a login manager object using Flask-Login
This contains the code that lets your application and Flask-Login work together, such as how to load a user from an ID, where to send users when they need to log in etc
e.g. in __init__.py near db = SQLAlchemy() add login_manager = LoginManager()
Initialise the plugin in the create_app() function in the same way as we did for the database e.g. login_manager.init_app(app)

Flask-Login requires the following properties and methods to be implemented:
is_authenticated: a property that is True if the user has valid credentials or False otherwise
is_active: a property that is True if the user's account is active or False otherwise
is_anonymous: a property that is False for regular users, and True for a special, anonymous user
get_id(): a method that returns a unique identifier for the user as a string (unicode, if using Python 2)
To make implementing a user class easier, you can inherit from UserMixin, which provides default implementations for all of these properties and methods.