# Using sessions in Flask

## Introduction to sessions

### What are sessions?

'Session' is an abstract concept to represent a series of HTTP requests and responses between a specific web browser and
server. HTTP doesn't support the notion of a session, but Python does.

A cookie is data stored on the client; a session's data is stored on the server (only 1 session per client).

Sessions are often built on top of cookies. The only data the client stores is a cookie holding a unique session ID on
each page request, the client sends its session ID cookie, and the server uses this to find and retrieve the client's
session data.

### How sessions are established

<img alt="sessions" src="img/session.png" width="500">

- Client's browser makes an initial request to the server.
- Server notes client's IP address/browser, stores some local session data, and sends a session ID back to client
- Client sends that same session ID back to server on future requests
- Server uses session ID to retrieve the data for the client's session later

### Sessions in Flask

[Sessions in Flask](https://flask.palletsprojects.com/en/1.1.x/quickstart/#sessions) are a way to store information
about a specific user from one request to the next. They work by storing a cryptographically signed cookie on the users
browser and decoding it on every request.

The session object can be treated just like a dictionary that persists across requests, making it an ideal place to
store non sensitive user data.

The user could look at the contents of your cookie but not modify it, unless they know the secret key used for signing.

However, the session object is NOT a secure way to store data. It's a base64 encoded string and can easily be decoded,
thus not making it a secure way to save or access sensitive information. An example of decoding the session data is
shown at the end
of [this tutorial by Julian Nash on pythonise.com](https://pythonise.com/series/learning-flask/flask-session-object).

### Using sessions in Flask

You must set a Flask secret key to use sessions e.g. in config.py:

```python
app.config["SECRET_KEY"] = “DkqwPYJSvITmwS_W0jvPzA”
# or
app.secret_key = `DkqwPYJSvITmwS_W0jvPzA`
```

To generate your own secret_key try the following in a Python console:

```python
import secrets

secrets.token_urlsafe(16)
```

For a production server you would also want to make the `SESSION_COOKIE_SECURE = True` to send cookie using secure HTTP

You then implement sessions using code similar to the following:

```python
# Import sessions from flask:
from flask import session

# Set session data: 
session['username'] = request.form['username’]
# Get session data: 
session['username’]
# Delete a session data: 
session.pop('username’)
```

## Using sessions in our example Flask app

Let's apply this to create a basic login/logout to our Flask app.

The Login/Logout routes in this example won't fully manage login and logout, all they will do is set and delete the
session cookie so that you can see how sessions work.

The secret key was set in `config.py` in an earlier activity so we do not need to create this again.

### 1. Modify the login route to set a session

The login form currently has email and password.

Modify the login route so that when the login form is submitted the session object is set with a 'name' parameter using
is the email address from the login form.

```python
session['name'] = request.form['email']
```

### 2. Modify the home page to get name from the session object
I have already removed the cookie code from the last exercise from the index route.

To set the name from the `session['name']` the route will look something like this:

```python
from flask import session


@main_bp.route('/', defaults={'name': 'Anonymous'})
@main_bp.route('/<name>')
def index(name):
    if 'name' in session:
        name = session['name']
    return render_template('index.html', title='Home page', name=name)

```

### 3. Create a logout route

Add a new route for logout to the auth module.

The route returns to the home page so we don't need to create a logout template.

```python
from flask import session


@auth_bp.route('/logout')
def logout():
    session.pop('name', None)
    return redirect(url_for('index'))
```

### 4. Test that it works and view the session cookie that is set
1. Start the Flask app

2. Open Chrome
   - Open the developer tools
   - Select the Application tab along the top of the toolbar
   - Select Cookies from the sidebar on the left

3. Login
   - Go to http://localhost:5000/login/ in Chrome.
   - Enter any email address and password and submit the form.
   - The index page should show the email address you just entered on the login form.
   - You should see the session in the Cookies section of the Developer Tools pane in Chrome.

4. Logout
   - enter http://localhost:5000/logout/

**Note**: You are unlikely to need to create sessions explicitly in the coursework.

The code that you just used will be replaced in the next activity when we use Flask-Login.

Flask-Login uses sessions however it creates and manages these for you.
