import dash_bootstrap_components as dbc
from dash import html

interpretLayout = dbc.Tab(className="global_tab",
                             # tab_style={"margin-left": "auto"},
                             label="Model Interpretation", children=[
                             html.P("A tab to allow model interpretation with model-agnostic methods.")
                         ])