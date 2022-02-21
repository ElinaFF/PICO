from dash import html
from dash.dependencies import Input, Output
import dash
import dash_bootstrap_components as dbc

from tabs import *

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX], meta_tags=[{"name": "viewport", "content": "width=device-width"}])
server = app.server
# app.scripts.config.serve_locally = False
app.css.config.serve_locally = False
app.config.suppress_callback_exceptions = True
app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})

infoTab = InfoTab(app)
splitsTab = SplitsTab(app)
mLTab = MLTab(app)
resultsTab = ResultsTab(app)
interpretTab = InterpretTab(app)


app.layout = html.Div(id="page", children=[
        html.Div(id="dataCache", children=[

        ],
        style={"display": "none"}
        ),
        html.Div(id="title_container", className="row", children=[
            html.Div(html.H1(id="title", children="MetaboDashboard"), id="title_bg")  #, style={"text-align": "center"}
        ]),
        html.Div(id="main-content", children=[
            dbc.Tabs(id="custom_big_tabs",
                     className="global_tabs_container",
                     children=[
                         infoTab.getLayout(),
                         splitsTab.getLayout(),
                         mLTab.getLayout(),
                         resultsTab.getLayout(),
                         interpretTab.getLayout()
                     ]
                     )
        ]),
    ])

if __name__ == "__main__":
    app.run_server(debug=True, port=8080, host='0.0.0.0')
