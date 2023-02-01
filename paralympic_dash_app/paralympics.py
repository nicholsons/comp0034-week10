""" This version creates all the charts in the main app file rather than in create_charts.py"""
from pathlib import Path
import pandas as pd
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px

#-------
# Charts
#-------

EVENT_DATA_FILEPATH = Path(__file__).parent.joinpath('data', 'events.csv')
MEDALS_DATA_FILEPATH = Path(__file__).parent.joinpath('data', 'all_medals.csv')

# Line chart showing how the number of events changed over time.

cols = ['REF', 'TYPE', 'YEAR', 'LOCATION', 'EVENTS', 'SPORTS', 'COUNTRIES', 'MALE', 'FEMALE', 'PARTICIPANTS']
df_events = pd.read_csv(EVENT_DATA_FILEPATH, usecols=cols)

line_events = px.line(df_events,
                          x='YEAR',
                          y='EVENTS',
                          color='TYPE',
                          labels={'YEAR': '', 'EVENTS': 'Number of events', 'TYPE': ''},
                          template="simple_white"
                          )


line_events.add_annotation(
    text="1984 held in New York & Stoke Mandeville",
    x=1984,
    y=1000,
    arrowhead=1,
    showarrow=True
)

# Stacked bar showing the ratio of male/female competitors over time for the winter paralympics.

# Add new columns that each contain the result of calculating the % of male and female participants
df_events['M%'] = df_events['MALE'] / df_events['PARTICIPANTS']
df_events['F%'] = df_events['FEMALE'] / df_events['PARTICIPANTS']

# Select just the Winter events
df_gender = df_events.loc[df_events['TYPE'] == "Winter"]

# Sort by year ascending
df_gender = df_gender.sort_values(['YEAR'], ascending=(True))

# Create a new column that combines Location and Year to use as the x-axis
df_gender['xlabel'] = df_gender['LOCATION'] + ' ' + df_gender['YEAR'].astype(str)

# Create the stacked bar plot of the % for male and female

stacked_bar_winter_gender = px.bar(df_gender,
                 x='xlabel',
                 y=['M%', 'F%'],
                 template="simple_white",
                 title='Winter paralympics',
                 labels={'xlabel': '', 'value': '', 'variable': ''},
                 )

stacked_bar_winter_gender.update_xaxes(ticklen=0)
stacked_bar_winter_gender.update_yaxes(visible=False, showticklabels=False)


# Create the mapbox chart

# Create the dataframe
map_cols = ['TYPE', 'YEAR', 'LOCATION', 'LAT', 'LON', 'PARTICIPANTS']
df_map_events = pd.read_csv(EVENT_DATA_FILEPATH, usecols=map_cols)

# Create the scatter_mapbox
mapbox_locations = px.scatter_mapbox(df_map_events,
lat="LAT",
lon="LON",
hover_name="LOCATION",
hover_data=['YEAR', 'TYPE'],
zoom=1,
mapbox_style="open-street-map",
size='PARTICIPANTS',
height=800,
width=1200,
color_discrete_sequence=['#F1C40F'],
)

# Remove the string wrapper ''' ''' to see the different style of map
'''
mapbox_locations.update_layout(
            mapbox_style='stamen-terrain',
            )
'''

#---------
# Dash app
#---------

app = Dash(__name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1"
        },
    ],
)

app.layout = dbc.Container(
    [
        html.H1("Paralympic Medals Dashboard"),
        html.H2("Has the number of athletes, nations, events and sports changed over time?"),
        dcc.Graph(
            id='line-sports',
            figure=line_events
        ),
        html.H2("Has the ratio of male and female athletes changed over time?"),
        dcc.Graph(
            id='bar-winter',
            figure=stacked_bar_winter_gender
        ),
        html.H2("Where in the world have the Paralympics have been held?"),
        dcc.Graph(
            id='map-locations',
            figure=mapbox_locations
        ),
    ],
    fluid=True,
)

if __name__ == '__main__':
    app.run_server(debug=True)
