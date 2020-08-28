# Add profiles to the community pages

In this activity you will allow users to save profile information about themselves and the provide a simple search that allows a user name to be searched for and the profile to be displayed as a result.

To achieve this you will need to:

- create a profile model class
- create a profile form class
- create templates for creating, updating and displaying a profile
- create routes for create_profile, edit_profile and display_profile
- create a route for search that searches the profile for matching usernames and returns a list of usernames
- modify the navbar so that when a person is logged in they have the option to create/edit their profile

While you may not have profile functionality in your coursework web app, this exercise will cover some new capabilities that you may need:

- using dropdowns in forms
- uploading, storing and retrieving images (using Flask-Reuploaded)
- generating webpages from database content
- a simple search using SQL queries

> **This activity is challenging**. You may want to attempt it in stages.

##### A note on using Flask-Reuploaded rather than Flask-Upload
To fully implement the ability to upload a profile image, the Flask documentation recommends using Flask-Uploads. 
However, this library is no longer being maintained and there is a conflict with the latest version of werkzeug (which Flask depends on).

Another library has been released that supersedes Flask-Uploads and addresses the werkzeug issue, [Flask-Reuploaded](https://pypi.org/project/Flask-Reuploaded/). 
This is in requirements.txt so you should already have this installed. 
Many of the code from tutorials for Flask-Upload will work still with Flask-Reuploaded.

You need to modify `config.py` and `__init__.py` in order to make use of Flask-Reuploaded. This has already been done for you.

## Create a profile model class

You will need to create a Profile class in the models.py which has a relationship with the User class.

```
id: Integer, primary key
username: Text, Unique, required
photo: Text
bio: Text
user_id: Integer, Foreign key (maps to the id field of the User class)
```

Each user can have only one profile, and each profile belongs to only one user. 
You will need to understand how to implement [one to one relationships in SQLAlchemy](https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#one-to-one) to define the relationship between the User (Parent) and the Profile (Child) classes.
Note that when you define the relationship in `models.py` you will use `db.relationship` rather than just `relationship`.

You can either choose to save the photo to a directory such as `static/photos` and store a reference to the file such as the filename in the database, or you can convert the image to binary data and store it as a blob. For this activity use the first approach as this will be consistent with the documentation for using Flask-Reuploaded and Flask-WTF.FileField in the next step of this activity.

Once you have created the Profile class you need to ensure that it is created in the database by adding the import to the `__init__.py` just before `db.create_all()`.

## Create a profile form class
Create a ProfileForm class for the community module e.g. in `community/forms.py`

The fields for a profile are:

- username: StringField, required, must be unique
- photo: [Flask-WTF FileField](https://flask-wtf.readthedocs.io/en/stable/form.html#module-flask_wtf.file) and NOT the wtf filefield, optional
- country: [QuerySelectField](http://wtforms.simplecodes.com/docs/0.6/ext.html#module-wtforms.ext.sqlalchemy.fields), optional
- bio: TextAreaField, optional

For the country field a list of countries has been added to example.sqlite in the country table. The code to add this is in `__init__.py`.

You should be able to work out how to create a form with the username and bio fields. 

The QuerySelectField is tricky to implement. The following solution provides: 
`query_factory` : the query that returns the list of countries (result objects)
`get_label` : the column that you want to use as the display of countries from the result, in this case `country_name`
`allow_blank` : set this to `True`, it places a blank at the start of the list

```python
country = QuerySelectField(label='Your location', query_factory=lambda: Country.query.all(),
                               get_label='country_name', allow_blank=True)
```

In the solution in week 8 I also added a custom validation to the username field to check that the username wasn't already in use. This is very similar to the validation you added to the signup form for the email field so you should be able to attempt to add this for the username too.

The FileField is more tricky that in first appears to fully implement as it relies on parameters that you also have to configure for Flask-Reuploaded.

So let's do that first. You will need to configure a location to save the photos in `config.py` and initialise parameters for the uploads in `my_app/__init__.py`.

In `config.py` in the Config class add the following which will set the path for photos to `my_app/static/photos`:

```python
class Config(object):
    UPLOADED_PHOTOS_DEST = pathlib.Path(__file__).parent.joinpath("static").joinpath("photos")
```

In `my_app/__init__.py`: 

- add the imports (note you still call it flask_uploads even though we are using Flask_Reuploaded) 
- create the global variable for photos (where you declare other globals such as `db = SQLAlchemy()`). The variable name `photos` matches to the `UPLOADED_PHOTOS_DEST` in `config.py` so don't change it to something else!
- configure the uploads for the app (e.g. where you initialise db, login manager etc)

The following shows only the code related to Flask_Reuploaded:

```python
from flask_uploads import UploadSet, IMAGES, configure_uploads

db = SQLAlchemy()
photos = UploadSet('photos', IMAGES)
# other code here


def create_app(config_classname):
    app = Flask(__name__)
    app.config.from_object(config_classname)

    db.init_app(app)
    configure_uploads(app, photos)

    # other code here
```

You can not close these two files and return to `community/forms.py`. 
You will need to import the `photos` global that you just created and the required imports.
The following example will create the FileField where the file is optional but if a file is provided then it has to be one of the types allowed by Flask_Uploads.IMAGES.

```python
from flask_wtf.file import FileField, FileAllowed
from my_app import photos

photo = FileField('Profile picture', validators=[FileAllowed(photos, 'Images only!')])
```

## Create templates
### Profile template

Since the process for create and update will be the same we can use one template for both purposes.

Create a template as you did for signup and login with the fields from the ProfileForm.

You will need to change the form tag:

- include the `enctype="multipart/form-data"` attribute to support the file upload
- don't set an action, this is because we will use the same form for two purposes so will determine the route based on criteria in the `process` route that renders the template rather than a different route.

Your form tag will look something like this:
````html
<form method="POST" action="" enctype="multipart/form-data">
````

## Create routes
### `profile` 

This route is actioned when a user tries to create a profile using `/community/profile`. If they already have a profile they are directed to the update_profile route, otherwise they are directed to the create_profile route.

The following is given in pseudo code. Try and work out the Python syntax for yourself.
```python
@community_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    # create a variable that is the result of a query. Query the Profile by joining the User and filtering where the user.id is the same as current_user.id. The structure of the query will be Profile.query.join().filter().first()
    # if there is a profile
        # return a redirect to the url_for community.update_profile
    # else
        # return a redirect to the url_for community.create_profile
```

Test it by signing up, logging in and then go to http://127.0.0.1:5000/community/profile
This should return a 404 error as neither of the routes exists yet.

### `create_profile`
This route provides a form to allow the user to create a new profile using the profile template you have already created.

If the form is validated on submit then find the user and add a profile associated with their account. You need to associate the user and profile as they are linked by keys in the database. The relationships that you defined in `models.py` come into play now.

The following code is explained for this route. You will need to understand this to be able to implement something similar in your coursework so don't just copy and paste without reading!.
```python
@community_bp.route('/create_profile', methods=['GET', 'POST'])
@login_required
def create_profile():
    form = ProfileForm() # This should be familiar from login and signup routes in auth
    if request.method == 'POST' and form.validate_on_submit():
        u = User.query.filter_by(id=current_user.id) # Find the current user
        filename = None # Set the filename for the photo to None since this is the default if the user hasn't chosen to add a profile photo
        if 'photo' in request.files: # Let's you check the submited form contains a photo (photo is the field name we used in the ProfileForm class)
            if request.files['photo'].filename != '': # As long as the filename isn't empty then save the photo
                filename = photos.save(request.files['photo']) # This saves the photo using the global variable photos to get the location to save to
        p = Profile(country=repr(form.country.data), username=form.username.data, photo=filename, bio=form.bio.data,
                    user_id=current_user.id) # Build a new profile to be added to the database based on the fields in the form
        db.session.add(p) # Add the new Profile to the database session
        db.session.commit() # This saves the new Profile to the database
        return redirect(url_for('community.display_profiles', username=p.username))
    return render_template('profile.html', form=form)
```

Test it by signing up, logging in and then go to http://127.0.0.1:5000/community/profile. 
You should be redirected to http://127.0.0.1:5000/community/create_profile
Fill out the profile form and press save.
You will need to check in the database to see if the profile was saved.

### `update_profile`
To update a profile means that the profile already exists. We can therefore pre-populate the profile form with the existing values (except for the file select field).

The following is a little crude as we overwrite all the fields each time regardless of whether a change was made.

```python
@community_bp.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    profile = Profile.query.join(User).filter_by(id=current_user.id).first() # Find the existing profile for this user
    form = ProfileForm(obj=profile) # Pre-populate the form by loading the profile using obj=. This relies on the field names in the Profile class in model matching the field names in the ProfileForm class, otherwise you have to explicitly state each field e.g. if the form used bio and the model used biography you would need to add  bio = profile.biography
    if request.method == 'POST' and form.validate_on_submit():
        if 'photo' in request.files:
            filename = photos.save(request.files['photo'])
            profile.photo = filename # Updates the photo field
        profile.country = form.country.data  # Updates the country field
        profile.bio = form.bio.data # Updates the bio field
        profile.username = form.username.data # Updates the user field
        db.session.commit() # Save the changes to the database
        return redirect(url_for('community.display_profiles', username=profile.username))
    return render_template('profiles.html', form=form)
```

### `display_profiles`
This route allows for an optional parameter, username, to be passed.
If we have created or updated a user profile then the route is used with the username parameter to display just that person's profile.
Otherwise we will search for any matching usernames and display the profiles of any that match.

In principle the route is quite straight foward as you are just querying profiles and returning a list of profile objects to the template.

The complexity arises with the display of the photos as only the filename is stored in the database and you need to translate this to a url that points to the image file.

In the following we do this by iterating through the profile query results, and creating a new list called urls to which we append the url for each photo.

We then use the python zip() function to pass both lists to the template.

```python
@community_bp.route('/display_profiles', methods=['POST', 'GET'])
@community_bp.route('/display_profiles/<username>/', methods=['POST', 'GET'])
@login_required
def display_profiles(username=None):
    results = None
    if username is None:
        if request.method == 'POST':
            term = request.form['search_term']
            if term == "":
                flash("Enter a name to search for")
                return redirect(url_for("community.index"))
            results = Profile.query.filter(Profile.username.contains(term)).all()
    else:
        results = Profile.query.filter_by(username=username).all()
    if not results:
        flash("No users found.")
        return redirect(url_for("community.index"))
    # The following iterates through the results and adds the full url to a list of urls
    urls = []
    for result in results:
        url = photos.url(result.photo)  # uses the global photos plus the photo file name to determine the full url path 
        urls.append(url)
    return render_template('display_profile.html', profiles=zip(results, urls)) # Note the zip to pass both lists as a parameter
```

## Create the display_profile template
Much of the following Jinja2 syntax you should be familiar with by now. 
However we haven't yet iterated through lists which is what the following provides an example of.

This uses a [Bootstrap card](https://getbootstrap.com/docs/4.0/components/card/) layout to display the profile(s).

```jinja2
{% extends 'base.html' %}
{% set title = 'Profile Display' %}
{% from "_formhelpers.html" import render_field %}
{% block content %}
    {% for result, url in profiles %}
        <div class="card" style="width: 18rem;">
            <img class="card-img-top" src="{{ url }}" alt="User profile photo">
            <div class="card-body">
                <h5 class="card-title">{{ result.username }}</h5>
                <h6>{{ result.country }}</h6>
                <p class="card-text">{{ result.bio }}</p>
            </div>
        </div>
    {% endfor %}
{% endblock %}
```

## Modify the navbar
### Enable the search in the navbar
We already have the routes that carries out the search, `display_profiles` so now we just need to enable our navbar.

Find the search form in the navbar template.

Change the form tag so the action is {{ url_for("community.display_profiles") }} and the method is post.

Try and search for a username. Did you get an error indicating you need to implement csrf protection?
This form wasn't created using FlaskForm, it is a simple HTML form, so you need to [implement the CSRF according to the documentation](https://flask-wtf.readthedocs.io/en/stable/csrf.html#html-forms).

This is a simplistic search and simply looks for matching usernames. 
If you want to implement a full text search then try [Miguel Grinberg's tutorial on using Elasticsearch with Flask](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvi-full-text-search).

### Add profile link to the navbar if a person is logged in
Modify the navbar so that when a person is logged in they have the option to select profile which maps to the roure for `profile`.
You already have similar code in the navbar so you should be able to work out how to do this.


> Well done! If you have got this far you should now have all the basic skills you are likely to need for coursework 2.