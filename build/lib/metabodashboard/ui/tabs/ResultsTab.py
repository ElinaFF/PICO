import glob
import json
import os
import time
from collections import Counter

import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
from dash import html, dcc, Output, Input, State, dash, Dash
import plotly.graph_objs as go
import pickle as pkl


from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

from metabodashboard.conf.MetaboDashboardConfig import STATISTICS
from .MetaTab import MetaTab
from metabodashboard.conf.LearnConfig import LEARN_CONFIG
from ...service import Plots
from metabodashboard.domain import MetaboController



class ResultsTab(MetaTab):
    def __init__(self, app: Dash, metabo_controller: MetaboController):
        super().__init__(app, metabo_controller)
        self.r = pkl.load(open("results.p", "rb"))
        self._plots = Plots("blues")

    def getLayout(self) -> dbc.Tab:
        __resultsMenuDropdowns = dbc.Card(className="results_menu_dropdowns", children=[
            dbc.CardBody([
                html.Div(className="dropdowns", children=[
                    html.H6("Experimental Design : "),
                    dbc.Select(id="design_dropdown",
                               className="form_select",
                               options=[{"label": "None", "value": "None"}],
                               value="None",
                               )]
                         ),
                html.Div(className="dropdowns", children=[
                    html.H6("ML Algorithm : "),
                    dbc.Select(id="ml_dropdown",
                               className="form_select",
                               options=[{"label": "None", "value": "None"}],
                               value="None",
                               )
                ]),
                dbc.Button("Load", color="primary", id="load_ML_results_button",
                           className="custom_buttons", n_clicks=0),
                html.Div(id="output_button_load_ML_results"),
            ],
                id="menu_results")

        ])

        __currentExperimentInfo = dbc.Card(children=[
            dbc.CardBody(children=[
                html.H6("Current experiment info"),  # , style={"marginTop": 25},
                html.Div(id="view_info", children=""),
                dcc.Loading(id="loading-1", children=[html.Div(id="loading-output-1")],
                            type="dot", color="#13BD00")
            ])
        ], className="w-25")

        _resultsInfo = html.Div(className="Results_info", children=[
            __resultsMenuDropdowns,
            __currentExperimentInfo,
        ])

        ___accuracyPlot = html.Div(className="acc_plot_and_title", children=[
            html.Div(className="title_and_help",
                     children=[html.H6("Accuracy plot"),
                               dbc.Button("[?]",
                                          className="text-muted",
                                          id="help_accPlot"),
                               dbc.Popover(children=[
                                   dbc.PopoverBody(
                                       "Blablabla wout wout")
                               ],
                                   id="pop_help_accPlot",
                                   is_open=False,
                                   target="help_accPlot")
                               ])
            ,
            dcc.Loading(dcc.Graph(id="accuracy_overview"),
                        type="dot", color="#13BD00")]
                                   )

        ___globalMetric = html.Div(className="w-25", children=[
            html.H6("Global metrics"),
            dcc.Loading(
                id="loading_global_metrics",
                children=html.Div(id="global_metrics",
                                  children=""),
                type="circle"),
            dbc.Button("Compute",
                       className="custom_buttons",
                       color="primary",
                       id="compute_global_metrics")
        ]

                                   )

        ___featuresTable = html.Div(className="table_features", children=[
            dcc.Loading(
                dbc.Table.from_dataframe(
                    df=pd.DataFrame({
                        "Feature": [],
                        "Number of models": []
                    }),
                    id="features_table",
                    striped=True, bordered=True,
                    hover=True)
            ),
        ])

        ___umap = html.Div(className="umap_plot_and_title",
                           children=[
                               html.Div(className="title_and_help",
                                        children=[html.H6("Umap"),
                                                  dbc.Button("[?]",
                                                             className="text-muted",
                                                             id="help_umapPlot"),
                                                  dbc.Popover(
                                                      children=[
                                                          dbc.PopoverBody(
                                                              "Blablabla wout wout")
                                                      ],
                                                      id="pop_help_umapPlot",
                                                      is_open=False,
                                                      target="help_umapPlot")
                                                  ]),
                               dcc.Loading(
                                   dcc.Graph(id="umap_overview"),
                                   type="circle")
                           ])

        __globalResultTab = dbc.Tab(className="sub_tab",
                                    label="Global results",
                                    children=[
                                        html.Div(className="fig_group",
                                                 children=[
                                                     ___accuracyPlot,
                                                     ___globalMetric
                                                 ]),
                                        html.Div(className="fig_group",
                                                 children=[
                                                     ___featuresTable,
                                                     ___umap
                                                 ])
                                    ])

        ___specificFilters = html.Div(className="fig_group_col", children=[
            html.Div(className="", children=[
                html.H6("Experiment number"),
                dbc.Select(id="experiment_dropdown",
                           className="form_select_large",
                           options=[
                               {"label": i, "value": i} for
                               i in
                               range(LEARN_CONFIG[
                                         "Nsplit"]
                                     )
                           ],
                           value="0"
                           ),
                html.H6("Show QCs"),
                dbc.Checklist(id="show_qc_checklist",
                              # switch=True,
                              options=[
                                  # Not sure how to label these
                                  {"label": "QC all run",
                                   "value": "true"}]
                              ),
                dbc.Button("Update", color="primary",
                           id="update_specific_results_button",
                           className="custom_buttons",
                           n_clicks=0),
                html.Div(
                    id="output_button_update_specific_results"),
            ]),
            html.Div(className="",
                     children=[
                         html.H6("Experiment metrics")
                     ])
        ])

        ___pcaPlot = html.Div(className="pca_plot_and_title", children=[
            html.Div(className="title_and_help",
                     children=[
                         html.H6("PCA", id="PCA_title"),
                         dbc.Button("[?]",
                                    className="text-muted",
                                    id="help_pcaPlot"),
                         dbc.Popover(children=[
                             dbc.PopoverBody(
                                 "Blablabla wout wout")
                         ],
                             id="pop_help_pcaPlot",
                             is_open=False,
                             target="help_pcaPlot")
                     ]
                     ),
            # Should we put the title on the plot?
            dcc.Loading(
                dcc.Graph(id="PCA",
                          figure=go.Figure(
                              data=[go.Scatter(
                                  x=[0, 1, 3, 4],
                                  y=[0, 2, 3, 4])],
                              layout=go.Layout(
                                  paper_bgcolor='rgba(0,0,0,0)',
                                  plot_bgcolor='rgba(0,0,0,0)'))
                          )
            )
        ])

        ___metaboliteLevelBoxplot = html.Div(className="bxplot_plot_select_and_title",
                                             children=[
                                                 html.Div(className="title_and_help",
                                                          children=[html.H6(
                                                              "Metabolite Level"),
                                                              dbc.Button("[?]",
                                                                         className="text-muted",
                                                                         id="help_BxPlot"),
                                                              dbc.Popover(
                                                                  children=[
                                                                      dbc.PopoverBody(
                                                                          "Blablabla wout wout")
                                                                  ],
                                                                  id="pop_help_BxPlot",
                                                                  is_open=False,
                                                                  target="help_BxPlot")
                                                          ]
                                                          ),
                                                 html.Div(id="metrics_table",
                                                          style={"margin": "auto",
                                                                 "display": "flex",
                                                                 "justify-content": "center"}),
                                                 html.Div(
                                                     id="metabolite_dropdown_container",
                                                     children=[
                                                         dbc.Select(
                                                             id="metabolite_dropdown",
                                                             className="form_select_large",
                                                             options=[],
                                                         )
                                                     ]),
                                                 dcc.Graph(id="metabo_boxplot",
                                                           figure=go.Figure(
                                                               data=[go.Box(
                                                                   x=[1, 2, 3, 4, 5, 5,
                                                                      5, 5, 5, 5, 5, 6,
                                                                      7,
                                                                      8]),
                                                                   go.Box(
                                                                       x=[10, 10, 10,
                                                                          10, 9, 9, 9,
                                                                          9, 9, 7,
                                                                          8, 5, 12, 12,
                                                                          15])],
                                                               layout=go.Layout(
                                                                   paper_bgcolor='rgba(0,0,0,0)',
                                                                   plot_bgcolor='rgba(0,0,0,0)')
                                                           )
                                                           )

                                             ])

        ___heatMap = html.Div(className="heatmap_plot_and_title",
                                                        children=[
                                                            html.Div(className="title_and_help",
                                                                     children=[html.H6("Heatmap",
                                                                                       id="heatmap_title"),
                                                                               dbc.Button("[?]",
                                                                                          className="text-muted",
                                                                                          id="help_heatmapPlot"),
                                                                               dbc.Popover(
                                                                                   children=[
                                                                                       dbc.PopoverBody(
                                                                                           "Blablabla wout wout")
                                                                                   ],
                                                                                   id="pop_help_heatmapPlot",
                                                                                   is_open=False,
                                                                                   target="help_heatmapPlot")
                                                                               ]
                                                                     ),
                                                            # Heat-map.
                                                            # Should we put the title on the plot?
                                                            dcc.Loading(children=[
                                                                html.Img(id='heatmap'),
                                                                # dcc.Graph(id="heatmap",
                                                                #    figure=go.Figure(
                                                                #        data=[
                                                                #            go.Scatter(
                                                                #                x=[0,1,3,4],
                                                                #                y=[0,2,3,4]
                                                                #            )
                                                                #        ]
                                                                #    )
                                                                # )
                                                            ]
                                                            )

                                                        ])

        __specificResultsTab = dbc.Tab(className="sub_tab",
                                       label="Specific results",
                                       children=[
                                           html.Div(className="fig_group", children=[
                                               ___specificFilters,
                                               ___pcaPlot
                                           ]),
                                           html.Div(className="fig_group", children=[
                                               ___metaboliteLevelBoxplot,
                                               ___heatMap
                                           ]),
                                       ]
                                       )

        _mainPlotContent = html.Div(id="main_plots-content", children=[  # className="six columns",
            dbc.Tabs(className="custom_sub_tabs",
                     children=[
                         __globalResultTab,
                         __specificResultsTab
                     ])
        ])

        return dbc.Tab(className="global_tab",
                       id="results_tab",
                       label="Results",
                       children=[
                           _resultsInfo,
                           _mainPlotContent
                       ])

    def _registerCallbacks(self) -> None:
        @self.app.callback(
            Output("pop_help_accPlot", "is_open"),
            [Input("help_accPlot", "n_clicks")],
            [State("pop_help_accPlot", "is_open")],
        )
        def toggle_popover(n, is_open):
            if n:
                return not is_open
            return is_open

        @self.app.callback(
            [Output("design_dropdown", "options"),
             Output("design_dropdown", "value")],
            [Input("custom_big_tabs", "active_tab")]
        )
        def update_results_dropdown_design(active):
            if active == "tab-3":
                f = os.listdir("Results/")
                a = [i.split(".pkl")[0].split("_")[:4] for i in f]
                a = ["_".join(i) for i in a]
                a = sorted(list(set(a)))
                return [{"label": i, "value": i} for i in a], a[0]
            else:
                return dash.no_update

        @self.app.callback(
            [Output("ml_dropdown", "options"),
             Output("ml_dropdown", "value")],
            [Input("custom_big_tabs", "active_tab")]
        )
        def update_results_dropdown_algo(active):
            if active == "tab-3":
                f = os.listdir("Results/")
                a = [i.split(".pkl")[0].split("_")[-1] for i in f]
                a = sorted(list(set(a)))
                return [{"label": i, "value": i} for i in a], a[0]
            else:
                return dash.no_update

        @self.app.callback(
            Output("loading-output-1", "children"),
            [Input("custom_big_tabs", "active_tab")]
        )
        def input_triggers_spinner(value):
            time.sleep(1)
            return

        @self.app.callback(
            Output("view_info", "children"),
            [Input("custom_big_tabs", "active_tab")],
            [State("ml_dropdown", "value"),
             State("design_dropdown", "value")]
        )
        def get_experiment_statistics(active, algo, design_name):
            if active == "tab-3":
                df = self.r[algo].results["info_expe"]
                return self._plots.show_exp_info_all(df)
            else:
                return dash.no_update

        @self.app.callback(
            Output("accuracy_overview", "figure"),
            [Input("load_ML_results_button", "n_clicks")],
            [State("ml_dropdown", "value"),
             State("design_dropdown", "value")]
        )
        def generates_accuracyPlot_global(n_clicks, algo, design_name):
            if n_clicks >= 1:
                df = self.r[algo].produce_accuracy_plot_all()
                return self._plots.show_accuracy_all(df)
            else:
                return dash.no_update

        @self.app.callback(
            [
                Output("features_table", "children"),
                Output("output_button_load_ML_results", "children")],
            [Input("load_ML_results_button", "n_clicks")],
            [State("ml_dropdown", "value"),
             State("design_dropdown", "value")]
        )
        def show_features(n_clicks, algo, design_name):
            if n_clicks >= 1:
                df = self.r[algo].produce_features_importance_table()
                return self._plots.show_features_selection(df), ""
            else:
                return dash.no_update

        @self.app.callback(
            [
                Output("umap_overview", "figure"),
                Output("output_button_load_ML_results", "children")],
            [Input("load_ML_results_button", "n_clicks")],
            [State("ml_dropdown", "value"),
             State("design_dropdown", "value")]
        )
        def show_umap(n_clicks, algo, design_name):
            if n_clicks >= 1:
                df = self.r[algo].produce_features_importance_table()
                return self._plots.show_umap_2D(df), ""
            else:
                return dash.no_update

        @self.app.callback(
            [
                # Output("accuracy_overview", "figure"),
                Output("overview_table", "children"),
                Output("umap_overview", "figure"),
                Output("output_button_load_ML_results", "children")],
            [Input("load_ML_results_button", "n_clicks")],
            [State("ml_dropdown", "value"),
             State("design_dropdown", "value")]
        )
        def show_global_view(n_clicks, ml_dropdown, design_dropdown):
            if n_clicks >= 1:
                print("Updating global accuracy plot")
                splits_name = []
                split_train_accuracy = []
                split_test_accuracy = []

                features = []
                data_matrix_filename = os.path.join("Results", design_dropdown + "_0_" + ml_dropdown + ".pkl")
                print("data_matrix_filename name found")
                with open(data_matrix_filename, "rb") as fi:
                    GS_rez = pkl.load(fi)
                    train_predict = pkl.load(fi)  # , encoding='bytes'
                    test_predict = pkl.load(fi)  # , encoding='latin1'
                    train_targets = pkl.load(fi)  # , encoding='latin1'
                    test_targets = pkl.load(fi)  # , encoding='latin1'

                print("data_matrix_filename red")

                # print("train predict : {}".format(train_predict))
                # cols = ["a"] * len(train_df[0])
                # train_df = pd.DataFrame(train_df, columns=cols)
                #
                # reducer = umap.UMAP()
                # print("umap initialized")

                def filter_cluster(df, threshold=0.5):
                    """
                    threshold : (proportion) minimum of non-zero values in a line to consider keeping this line
                    for example -> threshold = 0.6 means it will keep only the lines where there is at least 60% of non-zero values
                    """
                    df = df.T
                    nbr_col = len(df.columns.to_list())
                    print(nbr_col)
                    print((df.astype(bool).sum(axis=0)).shape)
                    df_filtered = df.loc[df.astype(bool).sum(axis=1) >= nbr_col * threshold]
                    return df_filtered.T

                # print(np.array(train_df).shape)
                # train_df = filter_cluster(train_df, threshold=1.0)
                # print(np.array(train_df).shape)
                # embedding = reducer.fit_transform(train_df)

                # trace_train = go.Scatter(
                #     x=embedding[:, 0],
                #     y=embedding[:, 1],
                #     mode="markers",
                #     text=np.array(train_df.index)
                # )
                # fig_umap = go.Figure(data=[trace_train],
                #                      layout=go.Layout(
                #                          paper_bgcolor='rgba(0,0,0,0)',
                #                          plot_bgcolor='rgba(0,0,0,0)')
                #                      )
                # return(fig, dash.no_update)

                for model_filename in glob.glob(
                        os.path.join("Results", design_dropdown + "_*_" + ml_dropdown + "*")):
                    with open(model_filename, "rb") as fi:
                        gc = pkl.load(fi)
                        print(gc.best_estimator_.classes_)
                        train_predict = pkl.load(fi)
                        test_predict = pkl.load(fi)

                    data_matrix_filename = os.path.join("Splits",
                                                        design_dropdown + "_" + model_filename.split("_")[1])
                    with open(data_matrix_filename, "rb") as fi:
                        train_df = pkl.load(fi)
                        train_targets = pkl.load(fi)
                        test_df = pkl.load(fi)
                        test_targets = pkl.load(fi)

                    splits_name.append(model_filename.split("_")[1])
                    split_train_accuracy.append(accuracy_score(y_true=train_targets, y_pred=train_predict))
                    split_test_accuracy.append(accuracy_score(y_true=test_targets, y_pred=test_predict))

                    if isinstance(gc.best_estimator_, RandomForestClassifier) or \
                            isinstance(gc.best_estimator_, DecisionTreeClassifier):
                        features_importance = gc.best_estimator_.feature_importances_

                    zipped = zip(features_importance, train_df.columns)
                    zipped = sorted(zipped, key=lambda t: t[0])

                    [features.append(i[1]) for i in zipped if np.abs(i[0]) > 0.0]

                features_count = Counter(features)

                # table = []
                # table_style = {"padding": "12px 55px", "text-align": "left"}
                # table.append(html.Tr([html.Th("Feature", style=table_style), html.Th("Number of models")]))
                # for f in features_count.most_common():
                #    table.append(html.Tr([html.Td(f[0]), html.Td(f[1])]))
                features_column = []
                n_models_column = []
                for f in features_count.most_common():
                    features_column.append(f[0])
                    n_models_column.append(f[1])

                df = pd.DataFrame()
                df["Feature"] = features_column
                df["Number of models"] = n_models_column

                trace_train = go.Scatter(
                    y=split_train_accuracy,
                    name="Train accuracy"
                )
                trace_test = go.Scatter(
                    y=split_test_accuracy,
                    name="Test accuracy"
                )
                fig_acc = go.Figure(data=[trace_train, trace_test])
                print("Number of items:{}".format(len(train_df.columns)))

                print("df : {}".format(df))
                df = pd.DataFrame({
                    "Feature": [],
                    "Number of models": []
                })

                return fig_acc, df, ""  # .to_dict("records"), fig_umap

            else:
                return dash.no_update

        @self.app.callback(
            Output("global_metrics", "children"),
            [Input("compute_global_metrics", "n_clicks"),
             Input("ml_dropdown", "value"),
             Input("design_dropdown", "value")]
        )
        def compute_global_metrics(n_clicks, ml_algo, exp_design):
            if n_clicks is None or n_clicks == 0:
                return dash.no_update
            if dash.callback_context.triggered[0]['prop_id'].split('.')[0] != "compute_global_metrics":
                return ""
            data_matrix_file_list = glob.glob(os.path.join("Splits", "{}_*".format(exp_design)))
            metrics_results_train = {i: [] for i in STATISTICS}
            metrics_results_test = {i: [] for i in STATISTICS}

            for data_matrix_filename in data_matrix_file_list:
                split_number = data_matrix_filename.split("_")[-1]
                model_filename = os.path.join("Results",
                                              "{}_{}_{}.pkl".format(exp_design, split_number, ml_algo))

                with open(data_matrix_filename, "rb") as fi:
                    train_df = pkl.load(fi, encoding="latin1")
                    train_targets = pkl.load(fi, encoding="latin1")
                    test_df = pkl.load(fi, encoding="latin1")
                    test_targets = pkl.load(fi, encoding="latin1")

                with open(model_filename, "rb") as fi:
                    gc = pkl.load(fi, encoding="latin1")
                    print(gc.best_estimator_.classes_)
                    train_predict = pkl.load(fi, encoding="latin1")
                    test_predict = pkl.load(fi, encoding="latin1")

                for stat in STATISTICS:
                    metrics_results_train[stat].append(
                        STATISTICS[stat](train_targets, train_predict)
                    )
                    metrics_results_test[stat].append(
                        STATISTICS[stat](test_targets, test_predict)
                    )
            table = []
            table_style = {"padding": "12px 55px", "text-align": "left"}
            table.append(html.Tr([html.Th("Metric", style=table_style), html.Th("Train"), html.Th("Test")]))
            for stat in STATISTICS:
                print(stat)
                train_average = np.average(metrics_results_train[stat])
                test_average = np.average(metrics_results_test[stat])
                train_std = np.std(metrics_results_train[stat])
                test_std = np.std(metrics_results_test[stat])
                print(train_average, train_std)
                table.append(html.Tr([html.Td(stat),
                                      html.Td("{:0.2f} ({:0.2f})".format(train_average, train_std)),
                                      html.Td("{:0.2f} ({:0.2f})".format(test_average, test_std))]
                                     ))
            return html.Table(table)

