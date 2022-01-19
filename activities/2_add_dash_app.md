# Adding a Dash app to a route in Flask

The [Dash app documentation](https://dash.plotly.com/integrating-dash) offers two solutions for running a Dash app
inside other apps, neither of which is suitable for the COMP0034 coursework. The first requires Dash Enterpise (you
don't have access to this), and the second requires a live hosted Dash app that you access in an iframe. Iframes are
generally discouraged and further you are not permitted to host a version of your app that could be accessed by others (
not allowed under the current UCL CS ethics approvals for data sets in this course).

The following solution is based on the 'Dash inside Flask' solution offered
by [Hackers and Slackers](https://hackersandslackers.com/plotly-dash-with-flask/) with some code from [ned](https://github.com/ned2/slapdash/tree/master/%7B%7Bcookiecutter.project_slug%7D%7D/src/%7B%7Bcookiecutter.project_slug%7D%7D).
Feel free to implement any other solution you may find.

They suggest moving the dash directory to within the flask directory. Their directory structure is:

```text
/plotlydash-flask-tutorial
├── /plotlyflask_tutorial
│   ├── __init__.py
│   ├── routes.py
│   ├── /static
│   ├── /templates
│   └── /plotlydash
│       └── dashboard.py
├── /data
├── README.md
├── config.py
├── requirements.txt
├── start.sh
└── wsgi.py
```

The `wsgi.py` in their example correlates to the `app.py` in the `my_flask_app` directory. The app.py doesn't need to be
edited.

Move the `paralympic_app` package into `my_flask_app`.

The Dash app needs to be modified so that the code is created through functions. In this example the functions are:
- `create_dash` which creates the Dash app instance
- `init_layout`  which defines the layout (also includes the code to create the charts), 
- `init_callbacks` which initialises the call backs.

The code in `paralympi_app.py` would look like that contained
in [/example_app/paralympic_app/paralympic_app.py](../example_app/paralympic_app/paralympic_app.py)

The `init_app()` function in their examples correlates to the `create_app()` function in our example app. This function
needs to be edited to import the Dash app, the code needs to be in a context so e.g.

```python
   with app.app_context():
    from example_app.models import User

    db.create_all()

    # Import Paralympics Dash application
    from .paralympic_app.paralympic_app import create_dash
    app = create_dash(app)

```

The route is then added to the navbar in navbar.html e.g.

```html

<li class="nav-item">
    <a class="nav-link" href="/dashboard/">Dashboard</a>
</li>
```