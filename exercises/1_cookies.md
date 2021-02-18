# Using cookies in Flask

## Introduction

HTTP is a stateless protocol; it simply allows a browser to request a single document from a web server.

Yet modern web apps rely on state data for authentication, user tracking, maintaining user preferences, shopping carts,
etc.

To achieve this we need some form of client related data storage.

Some commonly used options to achieve include [cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies)
and [Web Storage API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API). These are not the only
solutions.

The Web Storage API may be best suited to client-only data rather than client/server communications. Cookies are sent
with every HTTP request so requests can become bloated. It includes `localStorage` and `sessionStorage`
options. `localStorage` the data will last indefinitely unless is it manually deleted. Data in `sessionStorage` will
last for the current session. You can use JavaScript to save data using this method.

We are only going to cover cookies.

## Cookies

Cookies are small pieces of data that are either created on the client or sent by a server to a browser and saved
locally. They are attached by the browser to future HTTP requests. Cookies therefore allow for information to be stored
on the client in order to pass additional context to that server. A cookie's data consists of a single name/value pair.

Cookies are commonly used for user preferences that are common to most HTTTP requests, e.g. a language code, or
authorisation tokens.

You can typically see cookies that are sent with an HTTP request using the Developer Tools of a browser such as Chrome,
Firefox, Safari.

The following shows a Firefox browser viewing the cookies sent in a request to [the BBC website.](https://www.bbc.co.uk)

![cookies on the bbc site](img/bbc%20cookies.png)

### How long does a cookie exist?

- **Session cookie**: default type; a temporary cookie that is stored only in the browser's memory. When the browser is
  closed, cookies will be erased. They can not be used for tracking long-term information. No programs other than the
  browser can access them.

- **Persistent cookie**: one that is stored in a file on the browser's computer. Can track long-term information.
  Potentially less secure, because users (or programs they run) can open cookie files, see/change the cookie values,
  etc.

  There are a few flags that you can set when creating cookies that increase their security:
    - The `HttpOnly` flag prevents a cookie from being accessed using JavaScript; they are only accessible when being
      attached on HTTP requests. This helps to reduce the exposure of data through XSS (cross-site scripting) attacks.
      We will cover XSS in week 10.
    - the `Secure` flag ensures that a cookie is only sent when the request is sent over the HTTPS protocol.
    - The `SameSite` flag can be used to help prevent against CSRF (cross-site request forgery) requests. It tells the
      browser to only send the cookies if the request is to a URL on the same domain as the requester.

## Creating cookies in Flask

Working with cookies requires the following Flask imports:

- `request` To set and get cookies
- `make_response` To build a response to attach cookies to

```python
# Set a cookie
from flask import make_response, render_template


@app.route('/')
def index():
    response = make_response(render_template('index.html'))
    response.set_cookie('username', 'the username')
    return response


# Read a cookie
from flask import request


@app.route('/')
def index():
    username = request.cookies.get('username')
```

The syntax to set a cookie is `set_cookie(key, value="", max_age=None)` where

- `key` is the name of the cookie (required)
- `value` is the data you want to store in the cookie (defaults to empty string)
- `max_age` is the expiration time of the cookie in seconds, if not set the cookie will cease to exist when the user
  closes the browser
- `httponly` is optional and can be set to True or False. This hides the cookie from JavaScript and can help with XSS as
  an attacker's injected JavaScript would also not be able to see or read the cookie

So `set_cookie('foo', 'bar', max_age=60*60*24*365)` would set a cookie called ‘foo’ with a value of ‘bar’ to expire in 1
year.

## Example using cookies in Flask

This example builds on the signup code that was created last week.

The example works through the following steps:

- Create a cookie in the signup route as soon as a new user has been successfully created. The cookie should use the
  value of the first_name field from the form to create a cookie called name.
- To see the value of the cookie, modify the `index` page to display a welcome message with the name value if a cookie
  has been set. To read a cookie, you need to access the request object.
- Signup a new user. You should be directed to the `index` page after a successful signup which should have the
  content "Welcome <name>".
- Add a new route to delete the cookie, this is just so that we can see the effect on the index page after the cookie is
  deleted. To delete a cookie, you set its expiration as a date in the past.
- Go to http://127.0.0.1:5000/delete_cookie. You should be directed to the `index` page which should now display "
  Welcome".

### 1. Create a cookie in the signup route

Create a cookie in the signup route as soon as a new user has been successfully created.

The cookie should use the value of the first_name field from the form to create a cookie called name.

After creating the cookie, the user should be directed to the home page.

To set the cookie you need to:

- create a response (in this case the response is to redirect to the URL for the home page)
- set the cookie for the response, the cookie is called `name` and the value for the name is captured in the
  form.first_name field.
- return the response

You will need to add an import `from flask import make_response`.

Find the appropriate location in your signup route and add the following:

```python
from flask import make_response

response = make_response(redirect(url_for('main.index')))
response.set_cookie("name", user.firstname)
return response
```

We also need to change the `main.index` route to allow a `name` parameter to be passed:

```python
@main_bp.route('/', defaults={'name': 'Anonymous'})
@main_bp.route('/<name>')
def index(name):
    return render_template('index.html', title="Home page", name=name)
```

And modify the `index.html` to display the name parameter:

```html
{% extends 'layout.html' %}
{% block content %}
<h1>{{ title }}</h1>
<p>Welcome {{ name }}</p>
<p>This is the my_app home page.</p>
{% endblock %}
```

Run the Flask app to check that the `main.index` is displayed with the name 'Anonymous'.

### 2. Access the value of the cookie and pass it to the index page to customise the text

To see the value of the cookie, let's modify the `index` page to display a welcome message with the name value if a
cookie has been set.

To read a cookie, you need to access the request object.

```python 
@main_bp.route('/', defaults={'name': 'Anonymous'})
@main_bp.route('/<name>')
def index(name):
    if 'name' in request.cookies:
        name = request.cookies.get('name')
    return render_template('index.html', title='Home page', name=name)
```

Sign up a new user. You should be directed to the `index` page after a successful signup which should have the
content `Welcome! name`.

### 3. Add a new route to delete the cookie

This is only so that we can see the effect on the index page after the cookie is deleted.

To delete a cookie, you set its expiration as a date in the past.

```python
@main_bp.route('/delete_cookie')
def delete_cookie():
    response = make_response(redirect(url_for('main.index')))
    response.set_cookie('name', '', expires=datetime.now())
    return response
```

Go to http://127.0.0.1:5000/delete_cookie.

You should be directed to the `index` page which should now display `Welcome Anonymous`.


> **Note**: It is unlikely you will need to use cookies for the coursework. You can remove the above code from the signup route as we don't need it for any later activities.




