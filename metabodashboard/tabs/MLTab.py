import json
import os

import dash_bootstrap_components as dbc
import pandas as pd
from dash import html, State, Input, Output, dash

from metabodashboard.tabs.MetaTab import MetaTab
from metabodashboard.service.RunMLalgo import runAlgo
from metabodashboard.service.Utils import retrieve_data_from_sample_name


class MLTab(MetaTab):
    def getLayout(self) -> dbc.Tab:
        __splitConfigFile = html.Div(
            [
                dbc.Label("Name of splits config file *",
                          className="form_labels"),
                dbc.Input(id="name_splits_config", placeholder="Enter Name",
                          className="form_input_text"),
                dbc.FormText(
                    "Write a name for this batch of splits that will be used to identify its parameters file",
                ),
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
                dbc.Col(children=[__splitConfigFile, __CVConfig, __processNumberConfig
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
                                    children=[_definitionLearningConfig, _definitionLearningAlgorithm
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
            sklearn_algo_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "../conf/algo_sklearn.json"))

            if n >= 1:
                new_algo_name = name_new
                new_algo_params = {"function": name_new, "ParamGrid": {name_param: values_param},
                                   "importing": import_new}

                all_algo = {}
                with open(sklearn_algo_file, "r+") as algo_file:
                    data = json.load(algo_file)

                    data[new_algo_name] = new_algo_params
                    all_algo = data

                    algo_file.seek(0)
                    json.dump(data, algo_file)
                    algo_file.truncate()

                return [{"label": a, "value": a} for a in all_algo.keys()], "", "", "", ""

            else:
                all_algo = {}
                with open(sklearn_algo_file, "r+") as algo_file:
                    all_algo = json.load(algo_file)
                return [{"label": a, "value": a} for a in all_algo.keys()], "", "", "", ""

        @self.app.callback(
            Output("output_button_ml", "children"),
            [Input("start_learning_button", "n_clicks")],
            [State("in_algo_ML", "value"),
             State("name_splits_config", "value"),
             State("in_nbr_CV_folds", "value"),
             State("in_nbr_processes", "value")]
        )
        def start_machine_learning(n, selected_algos, split_config_file, cv_folds, nbr_process):
            if n >= 1:
                with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "../conf/algo_sklearn.json")), "r") as algo_file:
                    algo_list = json.load(algo_file)

                with open(split_config_file, "r") as conf_file:
                    splits_config = json.load(conf_file)

                print("Splits_dict 1er element = {}".format(
                    splits_config["Splits"][list(splits_config["Splits"].keys())[0]]))
                print("---")
                print("Data matrix type = {}".format(type(pd.read_json(splits_config["Data_matrix"]))))
                print("Data matrix 2 first lines = {}".format(pd.read_json(splits_config["Data_matrix"]).iloc[:2, :5]))

                # get all files : X_train files [0] and X_test files [1]
                # all_data_files = splits_config["Splits"]["split0"][0] + splits_config["Splits"]["split0"][1]

                # Check the processing needed and do it
                # ---> with SplitProcessing class

                # Then assign files to splits (create the actuals splits)
                # ---> with SplitProcessing class

                # Compute each algo for each split
                print("---> selected_algo type = {}".format(type(selected_algos)))
                print(selected_algos)
                l = []
                for a in selected_algos:
                    print("---> a = {}".format(a))
                    try:
                        algo = runAlgo(algo_list[a]["function"], cv_folds, algo_list[a]["ParamGrid"],
                                       algo_import=algo_list[a]["importing"])
                        print("instance algo créée avec importing")
                    except KeyError:
                        algo = runAlgo(algo_list[a]["function"], cv_folds, algo_list[a]["ParamGrid"])
                        print("instance algo créée sans importing")

                    dataframe = pd.read_json(splits_config["Data_matrix"])
                    for key, value in splits_config["Splits"].items():
                        opt_list = []
                        no = key.split("split")[-1]
                        print("no : {}".format(no))
                        Xtrain = retrieve_data_from_sample_name(value[0], dataframe)
                        opt_list.append(Xtrain)
                        Xtest = retrieve_data_from_sample_name(value[1], dataframe)
                        opt_list.append(Xtest)
                        opt_list.append(value[2])
                        opt_list.append(value[3])
                        opt_list.append(no)
                        l.append(opt_list)
                    print("liste l remplie")

                    for i in l:
                        print("learn {} split".format(i[-1]))
                        algo.learn(i)

                    print("finiiiiiiiii ---- !!!!!")

                    # pool = Pool(int(nbr_process))
                    # pool.map(algo.learn, l)

                return "Done!"

            else:
                return dash.no_update
