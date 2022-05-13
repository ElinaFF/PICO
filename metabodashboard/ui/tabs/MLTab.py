import json
import os

import dash_bootstrap_components as dbc
from dash import html, State, Input, Output, dash

from .MetaTab import MetaTab
from ...service import Utils


class MLTab(MetaTab):
    def getLayout(self) -> dbc.Tab:
        __splitConfigFile = html.Div(
            [
                dbc.Label("Select CV search type",
                          className="form_labels"),
                dbc.RadioItems(
                    options=[{"label": cv_type, "value": cv_type} for cv_type in self.metabo_controller.get_cv_types()],
                    value=self.metabo_controller.get_selected_cv_type(),
                    id="radio_cv_types"),
            ],
            className="form_field"
        )

        __CVConfig = html.Div([
            dbc.Label("Number of Cross Validation folds", className="form_labels"),
            dbc.Input(id="in_nbr_CV_folds", value="5", type="number", min=1,
                      size="5")
        ], className="form_field")

        __processNumberConfig = html.Div([
            dbc.Label("Number of processes"),
            dbc.Input(id="in_nbr_processes", value="2", type="number",
                      min=1,
                      size="5")
        ], className="form_field")

        _definitionLearningConfig = html.Div(className="title_and_form", children=[
            html.H4(id="Learn_conf_title", children="Define Learning configs"),
            dbc.Form(children=[
                dbc.Col(children=[__splitConfigFile,
                                  __CVConfig,
                                  __processNumberConfig
                                  ],
                        )
            ])
        ])

        __availableAlgorithms = html.Div(
            [
                dbc.Label("Available Algorithms", className="form_labels"),
                dbc.Checklist(id="in_algo_ML",
                              # inline=True
                              ),
            ],
            className="form_field"
        )

        __addCustomAlgorithm = html.Div(
            [
                dbc.Label("Add Sklearn Algorithms", className="form_labels"),
                dbc.Label("from sklearn.A import B"),
                dbc.Input(id="import_new_algo", placeholder="Complete import (A)",
                          className="form_input_text"),
                dbc.Input(id="name_new_algo", placeholder="Enter Name (B)",
                          className="form_input_text"),
                dbc.Label("Specify parameters to explore by gridsearch"),
                dbc.Input(id="name_param", placeholder="Name of parameter",
                          className="form_input_text"),
                dbc.Input(id="values_param", placeholder="Values to explore",
                          className="form_input_text"),
                dbc.Button("Add", color="success",
                           id="add_n_refresh_sklearn_algo_button",
                           className="custom_buttons", n_clicks=0),
            ],
            className="form_field"
        )

        __validationButton = html.Div(className="button_box", children=[
            html.Div(
                "Before clicking on the Learn button, make shure all field with an * are correctly filled."),
            dbc.Button("Learn", color="primary", id="start_learning_button",
                       className="custom_buttons", n_clicks=0),
            html.Div(id="output_button_ml", children="",
                     style={'display': 'none'}),

        ])

        _definitionLearningAlgorithm = html.Div(className="title_and_form", children=[
            html.H4(id="learn_algo_title", children="Define Learning Algorithms"),
            dbc.Form(children=[
                dbc.Col(children=[__availableAlgorithms, __addCustomAlgorithm, __validationButton
                                  ],
                        )
            ])
        ])

        return dbc.Tab(className="global_tab", label="Machine Learning",
                       children=[
                           html.Div(className="fig_group",
                                    children=[_definitionLearningConfig,
                                              _definitionLearningAlgorithm
                                              ]),
                       ])

    def _registerCallbacks(self) -> None:
        @self.app.callback(
            [Output("in_algo_ML", "options"),
             Output("import_new_algo", "value"),
             Output("name_new_algo", "value"),
             Output("name_param", "value"),
             Output("values_param", "value")],
            [Input("add_n_refresh_sklearn_algo_button", "n_clicks")],
            [State("import_new_algo", "value"),
             State("name_new_algo", "value"),
             State("name_param", "value"),
             State("values_param", "value")]
        )
        def add_refresh_available_sklearn_algorithms(n, import_new, name_new, name_param, values_param):
            sklearn_algo_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../conf/algo_sklearn.json"))

            if n >= 1:
                new_algo_name = name_new
                new_algo_params = {"function": name_new, "ParamGrid": {name_param: values_param},
                                   "importing": import_new}

                with open(sklearn_algo_file, "r+") as algo_file:
                    data = json.load(algo_file)

                    data[new_algo_name] = new_algo_params
                    all_algo = data

                    algo_file.seek(0)
                    json.dump(data, algo_file)
                    algo_file.truncate()

                return [{"label": a, "value": a} for a in all_algo.keys()], "", "", "", ""

            else:
                with open(sklearn_algo_file, "r+") as algo_file:
                    all_algo = json.load(algo_file)
                avail_algo = []
                for a in all_algo.keys():
                    if a == "SVM_L1" or a == "SCM" or a == "RandomSCM":
                        avail_algo.append({"label": a, "value": a, "disabled": True})
                    else:
                        avail_algo.append({"label": a, "value": a})
                return avail_algo, "", "", "", ""

        @self.app.callback(
            Output("output_button_ml", "children"),
            [Input("start_learning_button", "n_clicks")],
            [State("in_algo_ML", "value"),
             State("in_nbr_CV_folds", "value"),
             State("in_nbr_processes", "value")]
        )
        def start_machine_learning(n, selected_models, cv_folds, nbr_process):
            if n >= 1:
                print("in")
                print(selected_models)
                self.metabo_controller.set_selected_models(selected_models)
                self.metabo_controller.learn(int(cv_folds))

                Utils.dump_metabo_expe(self.metabo_controller._metabo_experiment)

                return "Done!"
            else:
                return dash.no_update

        @self.app.callback(
            Output("radio_cv_types", "value"),
            [Input("radio_cv_types", "value")]
        )
        def set_cv_type(value):
            self.metabo_controller.set_cv_type(value)
            return value
