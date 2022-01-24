import dash_bootstrap_components as dbc
from dash import html



infoLayout =  dbc.Tab(className="global_tab",
                                tab_style={"margin-left": "auto"},
                                label="Home", children=[
                                html.Div(className="fig_group", children=[
                                    html.Div(className="column_content", children=[

                                        dbc.Card(className="cards_info", children=[
                                            dbc.CardHeader("Splits"),
                                            dbc.CardBody(
                                                [
                                                    html.P("Blablabla",
                                                           className="card-text"),
                                                ]
                                            ),
                                        ]),
                                        dbc.Card(className="cards_info", children=[
                                            dbc.CardHeader("Machine Learning"),
                                            dbc.CardBody(
                                                [
                                                    html.P("Blablabla",
                                                           className="card-text"),
                                                ]
                                            ),
                                        ]),
                                        dbc.Card(className="cards_info", children=[
                                            dbc.CardHeader("results"),
                                            dbc.CardBody(
                                                [
                                                    html.P("Blablabla",
                                                           className="card-text"),
                                                ]
                                            ),
                                        ]),
                                        dbc.Card(className="cards_info", children=[
                                            dbc.CardHeader("Model interpretation"),
                                            dbc.CardBody(
                                                [
                                                    html.P("Blablabla",
                                                           className="card-text"),
                                                ]
                                            ),
                                        ]),
                                    ]),
                                    html.Div(className="column_content", children=[
                                        dbc.Card(className="card_body_fig", children=[
                                            # dbc.Card("Amazing figure here", className="card_body_fig", body=True),
                                            dbc.CardImg(src="/assets/Figure_home_wider.png", bottom=True)
                                        ])
                                    ])
                                ]),
                         ])