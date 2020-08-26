# Using cookies in Flask

This example works through the following steps:

1. Create a cookie in the signup route as soon as a new user has been successfully created. The cookie should use the value of the first_name field from the form to create a cookie called name. 
2. Add a new route to delete the cookie, this is just so that we can see the effect on the index page after the cookie is deleted. To delete a cookie, you set its expiration as a date in the past.
3. To see the value of the cookie, let's modify the `index` page to display a welcome message with the name value if a cookie has been set. To read a cookie, you need to access the request object. 
4. Signup a new user. You should be directed to the `index` page after a successful signup which should have the content "Welcome <name>".
5. Go to http://127.0.0.1:5000/delete_cookie. You should be directed to the `index` page which should now display "Welcome".

A change has been made to the `main.index` route to allow a `name` parameter to be passed:
```python
@main_bp.route('/')
@main_bp.route('/<name>')
def index(name=''):
    return render_template('index.html', title="Home page", name=name)
```

## 1. Create a cookie in the signup route 

Create a cookie in the signup route as soon as a new user has been successfully created. 

The cookie should use the value of the first_name field from the form to create a cookie called name. 

After creating the cookie, the user should be directed to the home page.

To set the cookie you need to: 

- create a response (in this case the response is to redirect to the URL for the home page)
- set the cookie for the response, the cookie is called `name` and the value for the name is captured in the form.first_name field.
- return the response

You will need to add an import `from flask import make_response`.

Find the appropriate location in your signup route and add the following:

```python
    response = make_response(redirect(url_for('main.index')))
    response.set_cookie("name", form.name.first_data)
    return response
```

## 2. Add a new route to delete the cookie

This is only so that we can see the effect on the index page after the cookie is deleted.

To delete a cookie, you set its expiration as a date in the past.

```python
@main_bp.route('/delete_cookie')
def delete_cookie():
    response = make_response(redirect(url_for('main.index')))
    response.set_cookie('name', '', expires=datetime.now())
    return response
```

## 3. Access the value of the cookie and pass it to the index page to customise the text

To see the value of the cookie, let's modify the `index` page to display a welcome message with the name value if a cookie has been set.

To read a cookie, you need to access the request object.
    ```python
    @main_bp.route('/')
    def index(name=""):
       if 'name' in request.cookies:
           name = request.cookies.get('name')
       return render_template('index.html', name=name)
    ```

## 4. Signup a new user

Sign up a new user. You should be directed to the `index` page after a successful signup which should have the content `Welcome! name`.

## 5. Delete the cookie

Go to http://127.0.0.1:5000/delete_cookie. 

You should be directed to the `index` page which should now display `Welcome!`.


> **Note**: It is unlikely you will need to use cookies for the coursework. You can remove the above code from the signup route as we don't need it for any later activities.