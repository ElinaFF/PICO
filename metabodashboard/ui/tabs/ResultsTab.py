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

from .MetaTab import MetaTab
from ...service import Plots
from ...domain import MetaboController


class ResultsTab(MetaTab):
    def __init__(self, app: Dash, metabo_controller: MetaboController):
        super().__init__(app, metabo_controller)
        self.r = pkl.load(open("big_results.p", "rb"))
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
                # html.Div(id="view_info", children=[
                dcc.Loading(
                    id="loading_expe_table",
                    children=html.Div(id="expe_table", children=""),
                    type="circle"),
                # dcc.Loading(id="loading-1", children=[html.Div(id="loading-output-1")],
                #             type="dot", color="#13BD00")
            ])
        ], className="w-25")

        _resultsInfo = html.Div(className="Results_info", children=[
            __resultsMenuDropdowns,
            __currentExperimentInfo,
        ])

        ___pcaPlot = html.Div(className="pca_plot_and_title", children=[
            html.Div(className="title_and_help",
                     children=[
                         html.H6("PCA", id="PCA_title"),
                         dbc.Button("[?]",
                                    className="text-muted btn-secondary",
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
            dcc.Loading(dcc.Graph(id="PCA"),
                        type="dot", color="#13BD00"),
            dcc.Slider(0, 3, 1, value=0, marks={0: "10", 1: "40", 2: "100", 3: "All"}, id="pca_slider")
        ])

        ___umap = html.Div(className="umap_plot_and_title",
                           children=[
                               html.Div(className="title_and_help",
                                        children=[html.H6("Umap"),
                                                  dbc.Button("[?]",
                                                             className="text-muted btn-secondary",
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
                               dcc.Loading(dcc.Graph(id="umap_overview"),
                                           type="dot", color="#13BD00"),
                               dcc.Slider(0, 3, 1, value=0, marks={0: "10", 1: "40", 2: "100", 3: "All"},
                                          id="umap_slider")

                           ])

        __dataResultTab = dbc.Tab(className="sub_tab",
                                  label="Data",
                                  children=[
                                      html.Div(className="fig_group",
                                               children=[
                                                   ___pcaPlot,
                                                   ___umap
                                               ]),

                                  ])

        ___accuracyPlot = html.Div(className="acc_plot_and_title", children=[
            html.Div(className="title_and_help",
                     children=[html.H6("Accuracy plot"),
                               dbc.Button("[?]",
                                          className="text-muted btn-secondary",
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
            html.H6("Global confusion matrix"),
            dcc.Loading(dcc.Graph(id="conf_matrix"),
                        type="dot", color="#13BD00")

        ])
        ___specificFilters = html.Div(className="fig_group_col", children=[
            html.Div(className="", children=[
                html.H6("Splits number"),
                dbc.Select(id="splits_dropdown",
                           className="form_select_large",
                           options=[{"label": "None", "value": "None"}],
                           value="None",
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
                         html.H6("Confusion matrix"),
                         dcc.Loading(dcc.Graph(id="split_conf_matrix"),
                                     type="dot", color="#13BD00")
                     ])
        ])
        ___metricsTable = html.Div(className="table_features", children=[
            dcc.Loading(
                id="loading_metrics_table",
                children=html.Div(id="metrics_score_table", children=""),
                type="circle"),
        ])

        __algoResultsTab = dbc.Tab(className="sub_tab",
                                   label="Algorithm",
                                   children=[
                                       html.Div(className="fig_group", children=[
                                           ___accuracyPlot,
                                           # ___globalMetric,
                                           ___metricsTable,
                                       ]),
                                       html.Div(className="fig_group", children=[
                                           ___specificFilters
                                       ]),

                                   ])

        __DTTreeTab = dbc.Tab(id="DTTT" ,className="sub_tab", label="DT Tree", disabled=True)

        ___featuresTable = html.Div(className="table_features", children=[
            dcc.Loading(
                id="loading_features_table",
                children=html.Div(id="features_table", children=""),
                type="circle"),

        ])
        ___metaboliteLevelBoxplot = html.Div(className="bxplot_plot_select_and_title",
                                             children=[
                                                 html.Div(className="title_and_help",
                                                          children=[html.H6(
                                                              "Metabolite Level"),
                                                              dbc.Button("[?]",
                                                                         className="text-muted btn-secondary",
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
                                                                className="text-muted btn-secondary",
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

        __featuresResultsTab = dbc.Tab(className="sub_tab",
                                       label="Features",
                                       children=[
                                           html.Div(className="fig_group", children=[
                                               ___featuresTable,
                                               ___metaboliteLevelBoxplot
                                           ]),
                                           html.Div(className="fig_group", children=[
                                               ___heatMap
                                           ]),
                                       ]
                                       )

        _mainPlotContent = html.Div(id="main_plots-content", children=[  # className="six columns",
            dbc.Tabs(className="custom_sub_tabs",
                     id="sub_tabs",
                     children=[
                         __dataResultTab,
                         __algoResultsTab,
                         __featuresResultsTab,
                         __DTTreeTab
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
                a = list(self.r.keys())
                return [{"label": i, "value": i} for i in a], a[0]
            else:
                return dash.no_update

        @self.app.callback(
            [Output("ml_dropdown", "options"),
             Output("ml_dropdown", "value")],
            [Input("design_dropdown", "value")],
            [State("custom_big_tabs", "active_tab")]
        )
        def update_results_dropdown_algo(design, active):
            if active == "tab-3":
                a = list(self.r[design].keys())
                return [{"label": i, "value": i} for i in a], a[0]
            else:
                return dash.no_update

        @self.app.callback(
            [Output("splits_dropdown", "options"),
             Output("splits_dropdown", "value")],
            [Input("sub_tabs", "active_tab")],
            [State("ml_dropdown", "value"),
             State("design_dropdown", "value")]
        )
        def update_nbr_splits_dropdown(active, algo, design):
            if active == "tab-1":
                a = list(self.r[design][algo].splits_number)
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
            Output("expe_table", "children"),
            [Input("load_ML_results_button", "n_clicks")],
            [State("ml_dropdown", "value"),
             State("design_dropdown", "value")]
        )
        def get_experiment_statistics(n_clicks, algo, design_name):
            if n_clicks >= 1:
                df = self.r[design_name][algo].results["info_expe"]
                table_body = self._plots.show_exp_info_all(df)
                return dbc.Table(table_body, id="table_exp_info", borderless=True,
                                 hover=True)  # dbc.Table.from_dataframe(df, borderless=True)
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
                df = self.r[design_name][algo].results["accuracies_table"]
                return self._plots.show_accuracy_all(df)
            else:
                return dash.no_update

        @self.app.callback(
            Output("features_table", "children"),
            [Input("load_ML_results_button", "n_clicks")],
            [State("ml_dropdown", "value"),
             State("design_dropdown", "value")]
        )
        def show_features(n_clicks, algo, design_name):
            if n_clicks >= 1:
                df = self.r[design_name][algo].results["features_table"].iloc[:10, :]
                return dbc.Table.from_dataframe(df, borderless=True)
            else:
                return dash.no_update

        @self.app.callback(
            Output("metrics_score_table", "children"),
            [Input("load_ML_results_button", "n_clicks")],
            [State("ml_dropdown", "value"),
             State("design_dropdown", "value")]
        )
        def show_metrics(n_clicks, algo, design_name):
            if n_clicks >= 1:
                df = self.r[design_name][algo].results["features_table"].iloc[:10, :]
                return dbc.Table.from_dataframe(df, borderless=True)
            else:
                return dash.no_update

        @self.app.callback(
            Output("umap_overview", "figure"),
            [Input("load_ML_results_button", "n_clicks"),
             Input("umap_slider", "value")],
            [State("ml_dropdown", "value"),
             State("design_dropdown", "value")]
        )
        def show_umap(n_clicks, slider_value, algo, design_name):
            if n_clicks >= 1:
                df = self.r[design_name][algo].results["umap_data"]
                classes = self.r[design_name][algo].results["classes"]
                print(slider_value)
                return self._plots.show_umap(df[slider_value], classes)
            else:
                return dash.no_update

        @self.app.callback(
            Output("conf_matrix", "figure"),
            [Input("load_ML_results_button", "n_clicks")],
            [State("ml_dropdown", "value"),
             State("design_dropdown", "value")]
        )
        def compute_conf_matrix(n_clicks, algo, design_name):
            if n_clicks >= 1:
                list_cm = []
                for s in self.r[design_name][algo].splits_number:
                    cm = self.r[design_name][algo].results[s]["Confusion_matrix"]
                    list_cm.append(cm[1])

                mean = np.mean(list_cm, axis=0)
                std = np.std(list_cm, axis=0)

                text_mat = []
                for i, line in enumerate(mean):
                    text_mat.append([])
                    for j, col in enumerate(line):
                        text_mat[i].append(str(col) + "(" + str(std[i][j]) + ")")

                labels = cm[0]
                return self._plots.show_general_confusion_matrix(mean, labels, text_mat)
            else:
                return dash.no_update

        @self.app.callback(
            Output("PCA", "figure"),
            [Input("load_ML_results_button", "n_clicks"),
             Input("pca_slider", "value")],
            [State("ml_dropdown", "value"),
             State("design_dropdown", "value")]
        )
        def show_pca(n_clicks, pca_value, algo, design_name):
            if n_clicks >= 1:
                df = self.r[design_name][algo].results["pca_data"]
                classes = self.r[design_name][algo].results["classes"]
                return self._plots.show_PCA(df[pca_value], classes)
            else:
                return dash.no_update

        @self.app.callback(
            Output("split_conf_matrix", "figure"),
            [Input("update_specific_results_button", "n_clicks")],
            [State("ml_dropdown", "value"),
             State("design_dropdown", "value"),
             State("splits_dropdown", "value")]
        )
        def compute_split_conf_matrix(n_clicks, algo, design_name, split):
            if n_clicks >= 1:

                cm = self.r[design_name][algo].results[split]["Confusion_matrix"][1]
                labels = self.r[design_name][algo].results[split]["Confusion_matrix"][0]

                text_mat = []
                for i, line in enumerate(cm):
                    text_mat.append([])
                    for j, col in enumerate(line):
                        text_mat[i].append(str(col))

                return self._plots.show_general_confusion_matrix(cm, labels, text_mat)
            else:
                return dash.no_update

        @self.app.callback(
            [Output("DTTT", "disabled"),
             Output("DTTT", "children")],
            [Input("load_ML_results_button", "n_clicks")],
            [State("ml_dropdown", "value"),
             State("design_dropdown", "value")]
        )
        def disable_DTTT(n_clicks, algo, design_name):
            if n_clicks >= 1:
                if algo == "DecisionTree":
                    model = self.r[design_name][algo]["best_model"]
                    return False, html.Img(src=self.app.get_asset_url("../assets/help_icon.png"))
            return True, ""
