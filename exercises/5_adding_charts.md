# Adding matplotlib and Plotly Express charts

The previous code examples assume that you are including a Dash app with charts.

You don't have to include your Dash app, you could simply include charts in the code of a Flask page.

This example adds two new routes to main for matplotlib and Plotly express charts.

A new dropdown menu option 'Charts' has been added to the navbar.

## Adding a matplotlib chart to a page

This is relatively simple and you may have already done this for coursework 1. You wil simply save the chart as animage
file and then display the image.

For example, add the following to main/routes.py:

```python
import matplotlib.pyplot as plt
from dash_app.recyclingchart import RecyclingChart
from dash_app.recyclingdata import RecyclingData


@main_bp.route('/mpl')
def mpl():
    data = RecyclingData()
    data.process_data_for_area('London')
    url = create_mpl_chart(period='2018/19', data=data)
    return render_template('chart_mpl.html', url=url, title="Matplotlib chart")


def create_mpl_chart(period, data):
    """Creates a matplotlib chart, saves as .png and returns the file path to the png"""
    data = data.recycling
    data = data.loc[data['Year'] == period]
    data = data.sort_values('Recycling_Rates', ascending=False)
    x = data['Area']
    y = data['Recycling_Rates']
    fig = plt.figure()
    ax = fig.subplots()
    ax.barh(x, y)
    ax.set_title(f'Recycling by area in {period}')
    ax.set_xlabel('Area')
    ax.set_ylabel('Recycling Rate')
    ax.tick_params(axis='x', labelsize='small')
    plt.tight_layout()
    url = 'static/img/plot.png'
    fig.savefig(url)
    return url
```

Create a template to display the chart e.g.

```html
{% extends 'layout.html' %}
{% block content %}
<img src={{url}} class="img-fluid" alt="Matplotlib chart">
{% endblock %}
```

Modify the navbar link to point to the new route:

```html

<li><a class="dropdown-item" href="{{ url_for(" main.mpl") }}">Matplotlib chart</a></li>
```

Note: Your browser may cache the image so if you try to improve the appearance of the image you may nee dto clear the
cache to see the changes.

## Integrating a Plotly chart

While Plotly Express charts can be created using Python, they are rendered using JavaScript.

To view the charts in a Flask route we need to:

1. Create and convert the chart to JSON and pass the JSON to the Jinja2 template
2. Use JavaScript with the Jinja template to display the chart

For this example we will re-use the code to create one of the Plotly Express charts from the dash_app.

## Create the route

Create the chart and a route using the code from one of the Plotly Express charts from the dash_app e.g.

```python
@main_bp.route('/px')
def px():
    plot = create_px_chart('London')
    return render_template('chart_px.html', plot=plot, title="Plotly Express chart")


def create_px_chart(area):
    """ Returns the plotly express chart in JSON"""
    data = RecyclingData()
    data.process_data_for_area(area)
    rc = RecyclingChart(data)
    fig = rc.create_chart(area)
    # Encode the plot as JSON
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_json
```


### Additional JS

You will need to use some JavaScript to display the chart. You can either add the following to your base template or you can add it
just to the chart template for your chart template.

```html

<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
```

I suggest editing `layout.html` to add an optional block where you can pass in JavaScript for a template to avoid
loading unnecessary libraries on every page. e.g. the layout.html <head> might look like this:

```html
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/bootstrap.css') }}">
    {% block javascript %}{% endblock %}
    <title>{{ title }}</title>
</head>
```

## Create the template for the chart

Create a Jinja2 template called `chart_px.html` and remember to pass the following Plotly js library to the block you just added to the layout
template e.g.

```html
{% extends 'layout.html' %}
{% block javascript %}
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
{% endblock %}
```
Now you need to add the content block to that `chart_px.html`. In the block you need to use some JavaScript which we haven't covered in the course:
```html
{% block content %}
    <div id="px_bar">
        <script>
            let graph = {{plot | safe}};
            Plotly.plot('px_bar', graph, {});
        </script>
    </div>
{% endblock %}
```
The `<script>` tag contains JavaScript code which does the following:
- The route passed in `plot` which is the px plot in JSON format. First it creates a JavaScript variable called `graph` from the JSON `plot`.
- Then it use the Plotly JavaScript library to render the chart and display it in the html div with the id of px_bar.

## Further reading
This won't be sufficient for all the chart elements you might be using such as range sliders. There are some blog posts
that may be useful e.g.:

[Recreating a Shiny App with Flask](https://www.jumpingrivers.com/blog/r-shiny-python-flask/)
