# Using Flask-Login

In this activity you will:

1. Configure the application to use Flask-Login
2. Add the required helper functions from UserMixin to the User class
3. Add the required helper functions to manage safe redirects and user loader functions to the auth routes
4. Add the routes for login and logout
5. Add login/logout to the navbar
6. Require a user to be logged in to access the community pages


## Configure the application to use Flask-Login

You have already completed some of the necessary config in week 5.

Go to `app/__init__.py` and review the code. You should see that a Login object for the app is being created. 

```python
from flask_login import LoginManager

login_manager = LoginManager()
```

The login manager now needs to be initialised for Flask in the `create_app()` function. It is currently commented out, remove the comment so the code looks like:
```python
def create_app(config_class=DevConfig):
       app = Flask(__name__)
       app.config.from_object(config_class)
   
       db.init_app(app)
       login_manager.init_app(app)
```

## Add the required helper functions to the User class

Flask-Login requires the following properties and methods to be implemented:

`is_authenticated`: a property that is `True` if the user has valid credentials or `False` otherwise

`is_active`: a property that is `True` if the user's account is active or `False` otherwise

`is_anonymous`: a property that is `False` for regular users, and `True` for a special, anonymous user

`get_id()`: a method that returns a unique identifier for the user as a string (unicode, if using Python 2)


Edit the User class in `models.py` to inherit UserMixin, you will also need to add the relevant import e.g. 
 ```python
from flask_login import UserMixin
        
class User(UserMixin, db.Model):
```

## Add the required helper functions 

### Helper functions to manage safe redirects 

Add the following from [Flask snippets](https://github.com/fengsp/flask-snippets/blob/master/security/redirect_back.py) to `auth.py`:

```python
   
from urllib.parse import urlparse, urljoin
from flask import request

def is_safe_url(target):
    host_url = urlparse(request.host_url)
    redirect_url = urlparse(urljoin(request.host_url, target))
    return redirect_url.scheme in ('http', 'https') and host_url.netloc == redirect_url.netloc


def get_safe_redirect():
    url = request.args.get('next')
    if url and is_safe_url(url):
        return url
    url = request.referrer
    if url and is_safe_url(url):
        return url
    return '/'

```
### Helper functions to manage loading the user

You will need the following function in order to be able to check whether a user is logged in on every page.

```python
from my_app import login_manager

@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None
```

The following can also be added to provide a customised message in the ebvent that a user is not logged in and they try to access a page that requires login:

```python
@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth.login'))
```

## Add the routes for login and logout

### Modify the login route

You will need to additional imports (shown in the snippet below).

When the login form is submitted and is valid then query the database to find the user. 

You can then use the `login_user()` function to login the user. Note that as we have a `remember me` checkbox in the login form then we need to pass additional parameters to login e.g.
`login_user(user, remember=form.remember.data, duration=timedelta(minutes=1))`. This is used so that if the user accidentally closes their browser they are not logged out, instead if they re-open the browser within a minute then they will still be logged in.

You then provide function to validate the `next` parameter (ie the URL you are going to next). If this isn't safe then the function will abort, otherwise the user will be logged in and redirected to the home page.

```python
from datetime import timedelta
from flask import abort
from flask_login import login_user

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user, remember=form.remember.data, duration=timedelta(minutes=1))
        next = request.args.get('next')
        if not is_safe_url(next):
            return abort(400)
        return redirect(next or url_for('main.index', name='user.firstname'))
    return render_template('login.html', form=form)
```

### Modify the `logout` route

Logout should only occur if a user is logged in, so use the `@login_required` decorator.

Flask-Login provides a `logout_user()` function.
    
```python
from flask_login import logout_user

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
```

## Add login/logout to the navbar

Modify the navbar so that when the user is not logged in the navbar displays login, whereas once they are logged in it should display logout.

The `is_anonymous` attribute was added to user objects when we inherited the UserMixin class.

The `current_user.is_anonymous` expression will be `True` when the user is not logged in.

We can use this to check which of the options to display in the navbar e.g.

```jinja2
{% if current_user.is_anonymous %}
    <li class="nav-item">
        <a class="nav-link" href="{{ url_for("auth.login") }}">Login</a>
    </li>
    <li class="nav-item">
         <a class="nav-link" href="{{ url_for("auth.signup") }}">Sign up</a>
    </li>
{% else %}
   <li class="nav-item">
       <a class="nav-link" href="{{ url_for("auth.logout") }}">Logout</a>
   </li>
{% endif %}
```

## Require a user to be logged in to access the community pages

You have already used the @login_required decorator to the logout function.

Add this to the community index page.

## Test it manually!

Restart the Flask app.

Try out the following:

- Sign up a new user
- Try to login with an incorrect email address (error message should be displayed on the form)
- Try to login with an incorrect password (error message should be displayed on the form)
- Logon with correct details and tick remember me
- Close the browser and reopen within a minute, you should still be logged in (logout shows in the navbar)
- Close the browser and wait longer than a minute, you should be logged out (login shows in the navbar)
- Choose Logout from the navbar, you should be logged out (login shows in the navbar)

> **Challenge**: can you write automated tests for these? 
