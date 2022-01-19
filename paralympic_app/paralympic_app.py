import dash
import json
from dash import html, Output, Input
from dash import dcc
from dash import dash_table
import dash_bootstrap_components as dbc

import create_charts as cc


fig_line_time = cc.line_chart_over_time('EVENTS')
fig_sb_gender_winter = cc.stacked_bar_gender("Winter")
fig_sb_gender_summer = cc.stacked_bar_gender("Summer")
fig_scatter_mapbox_OSM = cc.scatter_mapbox_para_locations("OSM")
fig_scatter_mapbox_USGS = cc.scatter_mapbox_para_locations("USGS")
df_medals_data = cc.top_ten_gold_data()
fig_top_ten_gold = cc.table_top_ten_gold_table(df_medals_data)
df_medals = cc.get_medals_table_data('London', 2012)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY])

app.layout = dbc.Container(
    [
        html.H1("Paralympic History"),
        html.H2("Has the number of athletes, nations, events and sports changed over time?"),

        dbc.Row([
            dbc.Col(width=2, children=[
                dcc.Dropdown(
                    id='type-dropdown',
                    options=[
                        {'label': 'Events', 'value': 'EVENTS'},
                        {'label': 'Sports', 'value': 'SPORTS'},
                        {'label': 'Countries', 'value': 'COUNTRIES'},
                        {'label': 'Athletes', 'value': 'PARTICIPANTS'},
                    ],
                    value='EVENTS'
                ),
            ]),
            dbc.Col(width=10, children=[
                dcc.Graph(
                    id='line-chart-time',
                    figure=fig_line_time
                ),
            ]),
        ]),
        html.H2("Has the ratio of male and female athletes changed over time?"),
        dbc.Row([
            dbc.Col(width=2, children=[
                dcc.Checklist(
                    id='mf-ratio-checklist',
                    options=[
                        {'label': 'Winter', 'value': 'Winter'},
                        {'label': 'Summer', 'value': 'Summer'}
                    ],
                    value=['Winter', 'Summer'],
                    labelStyle={"display": "inline-block"},
                ),
            ]),
            dbc.Col(width=10, children=[
                html.Div([
                    dcc.Graph(
                        id='stacked-bar-gender-win',
                        figure=fig_sb_gender_winter
                    )
                ], style={'display': 'block'}),
                html.Div([
                    dcc.Graph(
                        id='stacked-bar-gender-sum',
                        figure=fig_sb_gender_summer
                    )
                ], style={'display': 'block'}),
            ]),
        ]),

        html.H2("Where in the world have the Paralympics been held?"),
        dbc.Row([
            dbc.Col(width=2, children=[
                html.H3('Event highlights'),
                html.P('Hover on the points in the map to see the event highlights', id='highlight-text')
            ]),
            dbc.Col(width=10, children=[
                dcc.Graph(
                    id='scatter-mapbox-osm',
                    figure=fig_scatter_mapbox_OSM
                ),
            ]),
        ]),

        html.H2("Which countries have won the most gold medals since 1960?"),
        dash_table.DataTable(
            id='table-top-ten-gold-dash',
            columns=[{"name": i, "id": i}
                     for i in df_medals_data.columns],
            data=df_medals_data.to_dict('records'),
            style_cell=dict(textAlign='left'),
            style_header=dict(backgroundColor="lightskyblue"),
            style_data=dict(backgroundColor="white")
        ),

    ],
    fluid=True,
)


@app.callback(
    Output(component_id='line-chart-time', component_property='figure'),
    Input(component_id='type-dropdown', component_property='value')
)
def update_output_div(event_variable):
    """
    Call back for updating the line chart when the type of data to display is changed.

    :param event_variable: one of the following which are columns in the paralympics dataset ['EVENTS', 'SPORTS',
    'COUNTRIES', 'PARTICIPANTS']
    :return: plotly.px.Figure The line chart representing the chosen variable
    """
    fig_line_time = cc.line_chart_over_time(event_variable)
    return fig_line_time


@app.callback(
    [Output("stacked-bar-gender-win", "style"),
     Output("stacked-bar-gender-sum", "style")],
    Input("mf-ratio-checklist", "value"),
)
def show_hide_ratio_charts(selected_types):
    """
    Callback to display or hide the winter and summer male:female ratio bar charts depending on the checkbox values.

    :param selected_types: List of checkbox values for the event type(s) (Winter and/or Summer)
    :return: a list of values, the first sets visibility for the Winter chart, the second for the Summer
    """
    # Default to hiding both
    win_show = {'display': 'none'}
    sum_show = {'display': 'none'}
    if 'Winter' in selected_types:
        win_show = {'display': 'block'}
    if 'Summer' in selected_types:
        sum_show = {'display': 'block'}
    return [win_show, sum_show]


@app.callback(
    Output('highlight-text', 'children'),
    Input('scatter-mapbox-osm', 'hoverData'))
def display_hover_data(hoverData):
    """
    Callback to find the highlight text for a given paralympic event when it is hovered over on the map
    Uses the `hoverData` from the `dcc.Graph(id='scatter-mapbox-osm', figure=fig_scatter_mapbox_OSM),` to find the
    Location and Year of an event. The Location and Year are passed to a function called `get_event_highlights(
    location, year)` in `create_charts.py` that will get the highlight data. The data is then displayed in
    the `html.P('Click...', id='highlight-text')` element.
    :param hoverData: he `hoverData` from the Input
    :return: text for the paragraph with id='highlight-text'
    """
    location = json.dumps(hoverData['points'][0]['customdata'][2], indent=2)
    location = location.strip('"')
    year = json.dumps(hoverData['points'][0]['customdata'][3], indent=2)
    year = int(year)
    highlight_text = cc.get_event_highlights(location, year)
    return highlight_text


if __name__ == '__main__':
    app.run_server(debug=True)
