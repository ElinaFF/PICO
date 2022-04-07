import dash_bootstrap_components as dbc
from dash import html

from .MetaTab import MetaTab


class InfoTab(MetaTab):
    def getLayout(self) -> dbc.Tab:
        _splitsInfo = dbc.Card(className="cards_info", children=[
            dbc.CardHeader("Splits"),
            dbc.CardBody(
                [
                    html.P("In the Splits tab, you create a setting file with all info necessary to run a machine learning experiment. "
                           "This file will even contain path to a copy of the data to avoid broken paths (after some times, "
                           "files might be moved or deleted and the path pointing to their location will then be not valid). "
                    ),
                    html.P(
                           "It is at this step that you can decide the (potential) multiple design experiment that you wish to explore. "
                           "Indeed, in the case where you have 3 or more different labels (eg: healthy, sick, extremely sick or diet1, diet2, diet3, diet4), "
                           "you will be able to combine them in two groups (two classes) to confront the different conditions in different ways. "
                           "For example, can the algorithms differentiate/discriminate between diet1 vs all the others, or diet1 and diet2 vs diet3 and diet4, etc.",
                    ),
                ]
            ),
        ])

        _MLInfo = dbc.Card(className="cards_info", children=[
            dbc.CardHeader("Machine Learning"),
            dbc.CardBody(
                [
                    html.P("In this tab, you select the cross-validation parameters and the algorithms you wish to apply on your data."
                           "The cross-validation step is usefull to optimize the algorithm : it runs several time the algorithm on small"
                           "part of the dataset with different parameters, and will keep the best parameters/model which will be applied "
                           "to your real dataset and gives you the final results and analyses."

                           ),
                    html.P(
                           "For the algorithms selection, there is some already implemented by default in the tool, so you can simply "
                           "select them. But there is also the possibility to import manually other algorithms from Scikit-Learn, in this"
                           "case you need to provide several information about the algorithm you wish to add so it can be integrated in the "
                           "analysis."
                    ),
                    html.P(
                           "The possibility to add a completely custom algorithm will eventually also be available. But it will require "
                           "modifications directly in the code files, and thus? is meant for people with more informatics abilities."
                    ),
                ]
            ),
        ])

        _resultInfo = dbc.Card(className="cards_info", children=[
            dbc.CardHeader("Results"),
            dbc.CardBody(
                [
                    html.P("In this tab, ",
                           className="card-text"),
                ]
            ),
        ])

        # _interpretInfo = dbc.Card(className="cards_info", children=[
        #     dbc.CardHeader("Model interpretation"),
        #     dbc.CardBody(
        #         [
        #             html.P("Blablabla",
        #                    className="card-text"),
        #         ]
        #     ),
        # ])

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
                             children=[_splitsInfo, _MLInfo, _resultInfo]), _infoFigure])]) #_interpretInfo

    def _registerCallbacks(self) -> None:
        pass
