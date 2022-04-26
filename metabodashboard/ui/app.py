from dash import html
from dash.dependencies import Input, Output
import dash
import dash_bootstrap_components as dbc
import os
from ..service import Utils

from .tabs import *
from ..domain import MetaboController

PACKAGE_ROOT_PATH = os.sep.join(os.path.dirname(__file__).split(os.sep)[:-1])
DUMP_PATH = os.path.join(PACKAGE_ROOT_PATH, "domain", "dumps")
DUMP_EXPE_PATH = os.path.join(DUMP_PATH, "metaboExpe.p")


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX], meta_tags=[{"name": "viewport", "content": "width=device-width"}])
server = app.server
# app.scripts.config.serve_locally = False
app.css.config.serve_locally = False
app.config.suppress_callback_exceptions = True
app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})

metabo_controller = MetaboController(Utils.load_metabo_expe(DUMP_EXPE_PATH))
infoTab = InfoTab(app, metabo_controller)
splitsTab = SplitsTab(app, metabo_controller)
mLTab = MLTab(app, metabo_controller)
resultsTab = ResultsTab(app, metabo_controller)
interpretTab = InterpretTab(app, metabo_controller)


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
                         #interpretTab.getLayout()
                     ]
                     )
        ]),
    ])
