import dash_bootstrap_components as dbc
from dash import html

from metabodashboard.tabs.MetaTab import MetaTab


class InfoTab(MetaTab):
    def getLayout(self) -> dbc.Tab:
        _splitsInfo = dbc.Card(className="cards_info", children=[
            dbc.CardHeader("Splits"),
            dbc.CardBody(
                [
                    html.P("Blablabla",
                           className="card-text"),
                ]
            ),
        ])

        _MLInfo = dbc.Card(className="cards_info", children=[
            dbc.CardHeader("Machine Learning"),
            dbc.CardBody(
                [
                    html.P("Blablabla",
                           className="card-text"),
                ]
            ),
        ])

        _resultInfo = dbc.Card(className="cards_info", children=[
            dbc.CardHeader("Results"),
            dbc.CardBody(
                [
                    html.P("Blablabla",
                           className="card-text"),
                ]
            ),
        ])

        _interpretInfo = dbc.Card(className="cards_info", children=[
            dbc.CardHeader("Model interpretation"),
            dbc.CardBody(
                [
                    html.P("Blablabla",
                           className="card-text"),
                ]
            ),
        ])

        _infoFigure = html.Div(className="column_content", children=[
            dbc.Card(className="card_body_fig", children=[
                # dbc.Card("Amazing figure here", className="card_body_fig", body=True),
                dbc.CardImg(src="/assets/Figure_home_wider.png", bottom=True)
            ])
        ])

        return dbc.Tab(className="global_tab",
                       tab_style={"margin-left": "auto"},
                       label="Home", children=[
                html.Div(className="fig_group", children=[
                    html.Div(className="column_content",
                             # WARNING !! : _infoFigure is not with the card, it's in a separate column
                             children=[_splitsInfo, _MLInfo, _resultInfo, _interpretInfo]), _infoFigure])])

    def _registerCallbacks(self) -> None:
        pass
