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
```

```python
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

## Examples using cookies in Flask

It is unlikely you will need to implement cookies for your coursework.

If you want to experiment there are many tutorials and examples on the internet. The code for the first of those below
is in `sessions_and_cookies` app in the project folder:

- [Flask cookies](https://pythonise.com/series/learning-flask/flask-cookies)
- [Cookies in Flask](https://overiq.com/flask-101/cookies-in-flask/)
- [Cookies in Flask](https://cs.wellesley.edu/~webdb/lectures/cookies/index.html#cookies-in-flask)
