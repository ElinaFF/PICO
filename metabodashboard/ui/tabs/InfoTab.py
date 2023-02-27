import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Output, Input, State, callback_context

from .MetaTab import MetaTab
from ...service import decode_pickle_from_base64, Utils


class InfoTab(MetaTab):
    def getLayout(self) -> dbc.Tab:
        _docLink = dbc.Card(
            className="cards_info",
            children=[
                dbc.CardHeader("Documentation link"),
                dbc.CardBody(
                    [
                        "You can find the official documentation at this ",
                        html.A(
                            href="https://elinaff.github.io/MeDIC/",
                            target="_blank",
                            rel="noreferrer noopener",
                            children="link",
                        ),
                        ".",
                    ]
                ),
            ],
        )

        _splitsInfo = dbc.Card(
            className="cards_info",
            children=[
                dbc.CardHeader("Splits"),
                dbc.CardBody(
                    [
                        html.P(
                            "In the Splits tab, you create a setting file with all info necessary to run a machine learning experiment. "
                            "There is a hash mecanism in place to ensure that the locally saved data fits the experiment file "
                            "that might be loaded in the futur. This mecanism can be compared to a lock and key mecanism where the key "
                            "to check a file will only fit this particular file."
                        ),
                        html.P(
                            "It is at this step that you can decide the (potential) multiple design experiment that you wish to explore. "
                            "Indeed, in the case where you have 3 or more different labels (eg: healthy, sick, extremely sick or diet1, diet2, diet3, diet4), "
                            "you will be able to combine them in two groups (two classes) to confront the different conditions in different ways. "
                            "For example, can the algorithms differentiate/discriminate between diet1 vs all the others, or diet1 and diet2 vs diet3 and diet4, etc.",
                        ),
                    ]
                ),
            ],
        )

        _MLInfo = dbc.Card(
            className="cards_info",
            children=[
                dbc.CardHeader("Machine Learning"),
                dbc.CardBody(
                    [
                        html.P(
                            "In this tab, you select the cross-validation parameters and the algorithms you wish to apply on your data."
                            "The cross-validation step is usefull to optimize the algorithm : it runs several time the algorithm on small"
                            "part of the dataset with different parameters, and will keep the best parameters/model which will be applied "
                            "to your real dataset and gives you the final results and analyses."
                        ),
                        html.P(
                            "For the algorithms selection, there is some already implemented by default in the tool, so you can simply "
                            "select them. But there is also the possibility to import manually other algorithms from Scikit-Learn. In this "
                            "case you need to provide several information about the algorithm you wish to add so it can be integrated in the "
                            "analysis."
                        ),
                        html.P(
                            "The possibility to add a completely custom algorithm will eventually also be available. But it will require "
                            "modifications directly in the code files. It is meant for people with more programming abilities."
                        ),
                    ]
                ),
            ],
        )

        _resultInfo = dbc.Card(
            className="cards_info",
            children=[
                dbc.CardHeader("Results"),
                dbc.CardBody(
                    [
                        html.P(
                            "The entire section of Results is based on the perspective of analysing the features selected "
                            "by the algorithms. For one experimental design of classes, multiple algorithms can be run. "
                            "Then, the results and performances of each algorithm can be explored one by one to ensure that "
                            "the prediction and therefore the selection of the features is valid. At the end, there is a "
                            "section that aggregates the results of all the algorithms in several figures to compare which "
                            "features are selected by which algorithm and check for redundancies. The repeated use of a "
                            "metabolite across different algorithm is a good indicator of the relevance of this molecule.",
                            className="card-text",
                        ),
                    ]
                ),
            ],
        )

        # _interpretInfo = dbc.Card(className="cards_info", children=[
        #     dbc.CardHeader("Model interpretation"),
        #     dbc.CardBody(
        #         [
        #             html.P("Blablabla",
        #                    className="card-text"),
        #         ]
        #     ),
        # ])

        _loadExpe = dbc.Card(
            className="cards_info",
            style={"margin-left": "2em"},
            children=[
                dbc.CardHeader("Load MetaboExperiment"),
                dbc.CardBody(
                    [
                        html.P(
                            "You can load the file of a previous experiment and resume your analysis."
                        ),
                        dcc.Upload(
                            id="load_expe",
                            style={"width": "fit-content"},
                            children=[
                                dbc.Button(
                                    "Select File",
                                    id="load_expe_button",
                                    className="custom_buttons",
                                    color="primary",
                                    disabled=True,
                                )
                            ],
                        ),
                    ]
                ),
            ],
        )

        _infoFigure = dbc.Card(
            className="card_body_fig",
            children=[
                # dbc.Card("Amazing figure here", className="card_body_fig", body=True),
                dbc.CardImg(src="/assets/update_figure_steps_MeDIC_4.svg", bottom=True)
            ],
        )
        # TODO : add the filename
        _modal = dbc.Modal(
            children=[
                dbc.ModalHeader(
                    style={"padding": "2rem 3rem"},
                    children=[html.H6("Warning: STATIC VERSION")],
                ),
                dbc.ModalBody(
                    style={"padding": "2em"},
                    children=[
                        html.H3(
                            "Welcome to MeDIC demo version !",
                        ),
                        html.P(
                            "This is a static version, i.e. no experiments can be run. It is meant to give an overview of the results visualization possibilities. "
                        ),
                        html.P(children=[
                            "If you want to use the complete version, you can access the ",
                            html.A(
                                href="https://elinaff.github.io/MeDIC/",
                                target="_blank",
                                rel="noreferrer noopener",
                                children="official documentation",
                            ),
                            "."]
                        ),

                        #     Logo github and link to the github

                    ],
                ),
                dbc.ModalFooter(
                    html.A([
                        html.Img(
                            src='/assets/github-logo.png',
                            style={
                                'width': '1.5em',
                                'padding': 0,
                                'margin-right': '0.5em',
                            }),
                        html.Span(
                            "MeDIC on Github",
                            style={
                                'padding': 0,
                                'margin': 0
                            }
                        )
                    ], href='https://github.com/ElinaFF/MeDIC', target="_blank",
                        style={"display": "flex", "align-items": "center", "justify-content": "flex-end",
                               "width": "fit-content"}),
                )
            ],
            id="warning-not-match",
            size="lg",
            is_open=True,
        )

        _hidden_div = html.Div(id="hidden_div", style={"display": "none"})

        return dbc.Tab(
            className="global_tab",
            tab_style={"margin-left": "auto"},
            label="Home",
            children=[
                _modal,
                html.Div(
                    className="fig_group",
                    children=[
                        html.Div(
                            className="column_content",
                            # WARNING !! : _infoFigure is not with the card, it's in a separate column
                            children=[
                                _docLink,
                                _splitsInfo,
                                _MLInfo,
                                _resultInfo,
                                _hidden_div,
                            ],
                        ),
                        html.Div(
                            className="column_content",
                            children=[
                                _loadExpe,
                                _infoFigure,
                            ],
                        ),
                    ],
                ),
            ],
        )  # _interpretInfo