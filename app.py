import dash
import dash_core_components as dcc
import dash_html_components as html
import base64
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Defines names and paths for the images to be displayed in the Dash app

image_filename1 = 'exoplanets.png'
encoded_image1 = base64.b64encode(open('exoplanets.png', 'rb').read())

image_filename2 = 'cumuplanets.png'
encoded_image2 = base64.b64encode(open('cumuplanets.png', 'rb').read())

image_filename3 = 'numplanetsbydate.png'
encoded_image3 = base64.b64encode(open('numplanetsbydate.png', 'rb').read())

image_filename4 = 'numplanetsbydateandmethod.png'
encoded_image4 = base64.b64encode(open('numplanetsbydateandmethod.png', 'rb').read())

# Builds app

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

meta_tags = [{"name": "viewport", "content": "width=device-width, initial-scale=1"}],


app.layout = html.Div([
    html.H1("ExoDash", className="display-4", style={'textAlign': 'center'}),
    html.P("A daily digest of key exoplanetary information", className = "lead", style={'textAlign':'center'}),
    dbc.Nav(
        [
            dbc.NavLink("GitHub Repository", href="http://github.com/RobertsEng/ExoDash", active="exact"),

        ], horizontal = 'center'),
    html.Hr(),
    html.Div([
        html.Div([
            html.H2("Exoplanets Across the Galaxy"),
            html.Img(src='data:image/png;base64,{}'.format(encoded_image1.decode()), height=800),
            html.P("Green = Sun, Fuchsia = Stars with confirmed exoplanets", className = "lead", style={'textAlign':'center'}),
        ],style={'textAlign': 'center','padding':50}),

        html.Div([
            html.H2("Cumulative Number of Confirmed Exoplanets"),
            html.Img(src='data:image/png;base64,{}'.format(encoded_image2.decode()), height=800),

        ],style={'textAlign': 'center'}),
    ]),
    html.Div([
        html.Div([
            html.H2("Number of Confirmed Exoplanets by Year of Discovery"),
            html.Img(src='data:image/png;base64,{}'.format(encoded_image3.decode()), height=800)
        ],style={'textAlign': 'center'}),

        html.Div([
            html.H2("Number of Confirmed Exoplanets by Method of Discovery"),
            html.Img(src='data:image/png;base64,{}'.format(encoded_image4.decode()), height=800)
        ],style={'textAlign': 'center'}),
            ]),

])


app.run_server()