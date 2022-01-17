import pandas as pd
import numpy as np
import seaborn as sns
import io, base64, glob, datetime, json, importlib
from collections import Counter
from multiprocessing import Pool
import datetime
import time
import pickle as pkl

import dash, dash_bio
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_bootstrap_components as dbc

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score
import umap

import plotly.graph_objs as go

from LearnConfig import *
from ExperimentDesign import *
from Utils import *
from MetaboDashboardConfig import *

from LDTD_CardiaquesMTL_make_split import *
from SamplesPairing import SamplesPairing
from RunMLalgo import runAlgo
from DataFormat import DataFormat
from Utils import retrieve_data_from_sample_name

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX], meta_tags=[{"name": "viewport", "content": "width=device-width"}]) #"MetaboDashboard",
server = app.server
app.scripts.config.serve_locally = False
app.css.config.serve_locally = False
app.config.suppress_callback_exceptions = True
app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})


def layout():
    return html.Div(id="page", children=[
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
                        ##############
                        # Info tab #
                        ##############
                        dbc.Tab(className="global_tab",
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
                                            dbc.CardHeader("Results"),
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



                         ]),
                        #####################
                        # Splits Tab #
                        #####################
                        dbc.Tab(className="global_tab",
                             label="Splits", children=[
                                html.Div(className="fig_group_all_width", children=[
                                    dbc.Card(children=[
                                        dbc.CardBody(
                                            [
                                                html.Div(
                                                    "In this tab, you will create a setting file with all info necessary "
                                                    "to run a machine learning experiment. This file will even contain a copy of the data "
                                                    "to avoid broken paths (after some times, files might be moved or deleted and the path pointing "
                                                    "to their location will then be not valid). An * besides the name of the field means a value "
                                                    "is required, all other fields can be left untouched and will use default values."),
                                            ]
                                        ),
                                    ]),
                                ]),
                                html.Div(className="fig_group", children=[
                                    html.Div(className="title_and_form", children=[
                                        html.H4(id="CreateSplits_paths_title", children="A) Files"),
                                        dbc.Form(children=[
                                            dbc.Col(children=[
                                                dbc.FormGroup(
                                                    [
                                                        dbc.Label("Data file(s) *", className="form_labels"),
                                                        dbc.Input(id="path_to_data_file", placeholder="Enter path",
                                                                  className="form_input_text"),
                                                        dbc.FormText(
                                                            "Write the path to the data files (spectra). You can use either absolute or relative path.",
                                                        ),
                                                    ],
                                                    className="form_field"
                                                ),
                                                dbc.FormGroup(
                                                    [
                                                        dbc.Label("Metadata file *", className="form_labels"),
                                                        dbc.Input(id="in_path_to_metadata", placeholder="Enter path",
                                                                  debounce=True, className="form_input_text"),
                                                        dbc.FormText(
                                                            "Write the path of the metadata file.You can use either absolute or relative path. "
                                                            "Press Enter when you are done to update other forms.",
                                                        ),
                                                        html.Div(id="output_in_case_of_error_in_path_to_metadata")
                                                    ],
                                                    className="form_field"
                                                ),
                                                dbc.FormGroup(
                                                    [
                                                        dbc.Label("Output file *",
                                                                  className="form_labels"),
                                                        dbc.Input(id="name_splits_batch", placeholder="Enter Name",
                                                                  className="form_input_text"),
                                                        dbc.FormText(
                                                            "Write a unique name for the output file.",
                                                        ),
                                                    ],
                                                    className="form_field"
                                                ),
                                                dbc.FormGroup(
                                                    [
                                                        dbc.Label("Use raw data",
                                                                  className="form_labels"),
                                                        dbc.FormText(
                                                            "If there is normalized and raw data in your file, you can choose to use raw by selecting yes. "
                                                            "Default is no and will use normalized data",
                                                        ),
                                                        dbc.RadioItems(
                                                            id="in_use_raw",
                                                            options=[
                                                                {"label": "Yes", "value": True},
                                                                {"label": "No", "value": False}
                                                            ],
                                                            value=False,
                                                            labelCheckedStyle={"color": "#13BD00"},
                                                        )
                                                    ],
                                                ),

                                            ]),

                                        ]),

                                    ]),
                                    html.Div(className="title_and_form", children=[
                                        html.H4(id="sep_samples_title", children="B) Data Fusion"),
                                        dbc.Form(children=[
                                            dbc.Col(children=[
                                                dbc.FormText(
                                                    "A pattern for a positive file could be '_pos_' if the file name was"
                                                    " : sample1_pos_JH35.lcs it means that all positive files would have"
                                                    " the pattern in the middle of their name."),
                                                dbc.FormText(
                                                    "We consider that the name of a pos file is in all point identical"
                                                    " to the name of the neg file corresponding, except for the pos/neg"
                                                    " pattern. It is the same consideration for the other potential"
                                                    " pairing."
                                                ),
                                                html.Br(),
                                                dbc.FormGroup(
                                                    [
                                                        dbc.Checklist(
                                                            id="in_pairing_pos_neg",
                                                            options=[
                                                                {"label": "Pos and Neg pairing", "value": 0},
                                                            ],
                                                            labelCheckedStyle={"color": "#13BD00"},
                                                        )
                                                    ],
                                                ),
                                                html.Div(id="div_pair_pn", children=[
                                                    dbc.FormGroup(
                                                        [
                                                            dbc.Input(id="distinct_id_pos_samples",
                                                                      className="form_input_text",
                                                                      placeholder="Pattern for positive samples"),
                                                        ],
                                                    ),
                                                    dbc.FormGroup(
                                                        [
                                                            dbc.Input(id="distinct_id_neg_samples",
                                                                      className="form_input_text",
                                                                      placeholder="Pattern for negative samples"),
                                                        ],
                                                    ),
                                                ], style={'display': 'none'}),
                                                dbc.FormGroup(
                                                    [
                                                        dbc.Checklist(
                                                            id="in_pairing_samples",
                                                            options=[
                                                                {"label": "Other pairing", "value": 0},
                                                            ],
                                                            labelCheckedStyle={"color": "#13BD00"},
                                                        )
                                                    ],
                                                ),
                                                html.Div(id="div_pair_12", children=[
                                                    dbc.FormGroup(
                                                        [
                                                            dbc.Input(id="distinct_id_1_samples",
                                                                      className="form_input_text",
                                                                      placeholder="Pattern for type 1 of samples"),
                                                        ],
                                                    ),
                                                    dbc.FormGroup(
                                                        [
                                                            dbc.Input(id="distinct_id_2_samples",
                                                                      className="form_input_text",
                                                                      placeholder="Pattern for type 2 of samples"),
                                                        ],
                                                    ),
                                                ], style={"display": "none"}),

                                            ])
                                        ])
                                    ]),


                                ]),

                                html.Div(className="fig_group", children=[
                                    html.Div(className="title_and_form", children=[
                                        html.H4(id="Exp_desg_title", children="C) Define Experimental designs"),
                                        dbc.Form(children=[
                                            dbc.Col(children=[

                                                dbc.FormText(
                                                    "Allows to link each file to its type/group to separate them approprietly afterwards."
                                                ),
                                                dbc.Card([
                                                    dbc.FormGroup(
                                                        [
                                                            dbc.Label("Name of the targets column"),
                                                            dbc.RadioItems(id="in_target_col_name", value=0,
                                                                           inline=True),
                                                        ],
                                                        className="form_field"
                                                    ),
                                                    dbc.FormGroup(
                                                        [
                                                            dbc.Label("Name of the unique id column"),
                                                            dbc.RadioItems(id="in_ID_col_name", value=0, inline=True),
                                                        ],
                                                        className="form_field"
                                                    )],
                                                    body=True
                                                ),
                                                html.Br(),
                                                dbc.FormText(
                                                    "Define labels and filter out samples."
                                                ),
                                                dbc.Card(id="", children=[
                                                    dbc.FormGroup(
                                                        [
                                                            dbc.Label("Type of classification"),
                                                            dbc.RadioItems(id="in_classification_type", value=0,
                                                                           inline=True,
                                                                           options=[
                                                                               {"label": "Binary", "value": 0},
                                                                               {"label": "Multiclass", "value": 1,
                                                                                "disabled": True},
                                                                           ]),
                                                        ],
                                                        className="form_field"
                                                    ),
                                                    dbc.FormGroup(
                                                        [
                                                            dbc.Label("Labels"),
                                                            html.Div(className="fig_group_mini",
                                                                     id="define_classes_desgn_exp", children=[
                                                                    dbc.Input(id="class1_name"),
                                                                    dbc.Checklist(id="possible_groups_for_class1"),
                                                                    dbc.Input(id="class2_name"),
                                                                    dbc.Checklist(id="possible_groups_for_class2")
                                                                ])
                                                        ],
                                                        className="form_field"
                                                    ),
                                                    dbc.Button("Add", id="btn_add_design_exp", color="primary",
                                                               className="custom_buttons", n_clicks=0),
                                                    html.Div(id="output_btn_add_desgn_exp")

                                                ], body=True),
                                            ]),

                                        ]),

                                    ]),
                                    html.Div(className="title_and_form", children=[
                                        html.H4(id="Define_split_title", children="D) Define splits"),
                                        dbc.Form(children=[
                                            dbc.Col(children=[
                                                dbc.FormGroup([
                                                    dbc.Label("Proportion of samples in test"),
                                                    dbc.Input(id="in_percent_samples_in_test", value="0.2",
                                                              type="number",
                                                              min=0, max=1, step=0.01,
                                                              size="5")
                                                ], className="form_field"),
                                                dbc.FormGroup([
                                                    dbc.Label("Number of splits"),
                                                    dbc.Input(id="in_nbr_splits", value="25", type="number", min=1,
                                                              size="5"),
                                                ], className="form_field"),
                                                dbc.FormGroup([
                                                    dbc.Label("Peak Threshold"),
                                                    dbc.Input(id="in_peak_threshold_value", value="500", type="number",
                                                              min=1,
                                                              size="5")
                                                ], className="form_field"),
                                                dbc.FormGroup([
                                                    dbc.Label("AutoOptimize number"),
                                                    dbc.Input(id="in_autoOptimize_value", value="20", type="number",
                                                              min=1,
                                                              size="5")
                                                ], className="form_field"),
                                            ]),
                                        ])
                                    ]),

                                ]),
                                html.Div(className="fig_group", children=[
                                    html.Div(className="title_and_form", children=[
                                        html.H4(id="preprocess_title", children="E) Other Preprocessing"),
                                        dbc.Form(children=[
                                            dbc.Col(children=[
                                                dbc.FormText(
                                                    "Options in case of LDTD data that needs to be preprocess"),
                                                dbc.Collapse(
                                                    dbc.Card(
                                                        dbc.CardBody(
                                                            children=[
                                                                dbc.FormGroup(
                                                                    [
                                                                        dbc.Label("Processing according to data type"),
                                                                        dbc.FormText(
                                                                            "LDTD1 means the preprocessing will be done on all samples in one time. "
                                                                            "LDTD2 means the preprocessing will be done seperatly for each split."),
                                                                        dbc.RadioItems(id="in_type_of_data", value="none",
                                                                                       inline=True,
                                                                                       options=[
                                                                                           {"label": "None", "value": "none"},
                                                                                           {"label": "LDTD 1", "value": "LDTD1"},
                                                                                           {"label": "LDTD 2", "value": "LDTD2"},
                                                                                       ]),
                                                                    ],
                                                                    className="form_field"
                                                                ),
                                                                dbc.FormGroup(
                                                                    [
                                                                        dbc.Label("Perform peak picking"),
                                                                        dbc.RadioItems(id="in_peak_picking", value=0,
                                                                                       inline=True,
                                                                                       options=[
                                                                                           {"label": "No", "value": 0,
                                                                                            "disabled": True},
                                                                                           {"label": "Yes", "value": 1,
                                                                                            "disabled": True},
                                                                                       ]),
                                                                    ],
                                                                    className="form_field"
                                                                ),
                                                                dbc.FormGroup(
                                                                    [
                                                                        dbc.Label("Perform alignment"),
                                                                        dbc.RadioItems(id="in_alignment", value=0,
                                                                                       inline=True,
                                                                                       options=[
                                                                                           {"label": "No", "value": 0,
                                                                                            "disabled": True},
                                                                                           {"label": "Yes", "value": 1,
                                                                                            "disabled": True},
                                                                                       ]),
                                                                    ],
                                                                    className="form_field"
                                                                ),
                                                                dbc.FormGroup(
                                                                    [
                                                                        dbc.Label("Perform normalization"),
                                                                        dbc.RadioItems(id="in_normalization", value=0,
                                                                                       inline=True,
                                                                                       options=[
                                                                                           {"label": "No", "value": 0,
                                                                                            "disabled": True},
                                                                                           {"label": "Yes", "value": 1,
                                                                                            "disabled": True},
                                                                                       ]),
                                                                    ],
                                                                    className="form_field"
                                                                ),
                                                            ]
                                                        )
                                                    ),
                                                    id="collapse_preprocessing",
                                                ),
                                                dbc.Button(
                                                    "Open",
                                                    id="collapse_preprocessing_button",
                                                    className="custom_buttons",
                                                    color="primary",
                                                    n_clicks=0
                                                ),

                                            ])
                                        ])
                                    ]),
                                    html.Div(className="title_and_form", children=[
                                        html.H4(id="create_split_title", children="F) Generate file"),
                                        dbc.Form(children=[
                                            dbc.Col(children=[
                                                html.Div(id="output_button_split_file"),
                                                html.Div(className="button_box", children=[
                                                    html.Div("Before clicking on the Create button, make shure all field with an * are correctly filled."),
                                                    dbc.Button("Create", color="primary", id="split_dataset_button",
                                                               className="custom_buttons", n_clicks=0),
                                                    html.Div(id="output_button_split", children="",
                                                             style={'display': 'none'}),

                                                ]),

                                            ])
                                        ])
                                    ])
                                ]),


                         ]),
                        ##########
                        # ML Tab #
                        ##########
                        dbc.Tab(className="global_tab", label="Machine Learning",
                                children=[
                                    html.Div(className="fig_group", children=[

                                        html.Div(className="title_and_form", children=[
                                            html.H4(id="Learn_conf_title", children="Define Learning configs"),
                                            dbc.Form(children=[
                                                dbc.Col(children=[
                                                    dbc.FormGroup(
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
                                                    ),
                                                    dbc.FormGroup([
                                                        dbc.Label("Number of Cross Validation folds", className="form_labels"),
                                                        dbc.Input(id="in_nbr_CV_folds", value="5", type="number", min=1,
                                                                  size="5")
                                                    ], className="form_field"),
                                                    dbc.FormGroup([
                                                        dbc.Label("Number of processes"),
                                                        dbc.Input(id="in_nbr_processes", value="2", type="number",
                                                                  min=1,
                                                                  size="5")
                                                    ], className="form_field"),

                                                ],
                                                )
                                            ])
                                        ]),
                                        html.Div(className="title_and_form", children=[
                                            html.H4(id="learn_algo_title", children="Define Learning Algorithms"),
                                            dbc.Form(children=[
                                                dbc.Col(children=[
                                                    dbc.FormGroup(
                                                        [
                                                            dbc.Label("Available Algorithms", className="form_labels"),
                                                            dbc.Checklist(id="in_algo_ML",
                                                                          # inline=True
                                                                          ),
                                                        ],
                                                        className="form_field"
                                                    ),
                                                    dbc.FormGroup(
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
                                                    ),
                                                    html.Div(className="button_box", children=[
                                                        html.Div(
                                                            "Before clicking on the Learn button, make shure all field with an * are correctly filled."),
                                                        dbc.Button("Learn", color="primary", id="start_learning_button",
                                                                   className="custom_buttons", n_clicks=0),
                                                        html.Div(id="output_button_ml", children="",
                                                                 style={'display': 'none'}),

                                                    ]),

                                                ],
                                                )
                                            ])
                                        ]),
                                    ]),
                                ]),
                        ###############
                        # Results Tab #
                        ###############
                        dbc.Tab(className="global_tab",
                                id="results_tab",
                                label="Results",
                                children=[
                                    html.Div(className="Results_info", children=[
                                        dbc.Card(className="results_menu_dropdowns", children=[
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

                                        ]),
                                        dbc.Card(children=[
                                            dbc.CardBody(children=[
                                                html.H6("Current experiment info"),  # , style={"marginTop": 25},
                                                html.Div(id="view_info", children=""),
                                                dcc.Loading(id="loading-1", children=[html.Div(id="loading-output-1")],
                                                            type="dot", color="#13BD00")
                                            ])
                                        ], className="w-25"),
                                    ]),

                                    html.Div(id="main_plots-content", children=[  # className="six columns",
                                        dbc.Tabs(className="custom_sub_tabs",
                                            children=[
                                            dbc.Tab(className="sub_tab",
                                                label="Global Results",
                                                children=[
                                                    html.Div(className="fig_group", children=[
                                                        html.Div(className="acc_plot_and_title", children=[
                                                            html.Div(className="title_and_help", children=[html.H6("Accuracy plot"),
                                                                      dbc.Button("[?]", className="text-muted", id="help_accPlot"),
                                                                      dbc.Popover(children=[
                                                                          dbc.PopoverBody("Blablabla wout wout")
                                                                      ],
                                                                          id="pop_help_accPlot",
                                                                          is_open=False,
                                                                          target="help_accPlot")
                                                                      ])
                                                            ,
                                                            dcc.Loading(dcc.Graph(id="accuracy_overview"),
                                                                        type="dot", color="#13BD00")]
                                                        ),
                                                        html.Div(className="w-25", children=[
                                                            html.H6("Global metrics"),
                                                            dcc.Loading(
                                                                id="loading_global_metrics",
                                                                children=html.Div(id="global_metrics", children=""),
                                                                type="circle"),
                                                            dbc.Button("Compute", className="custom_buttons",
                                                                       color="primary", id="compute_global_metrics")
                                                            ]
                                                        )
                                                        ]
                                                    ),
                                                    html.Div(className="fig_group", children=[
                                                        html.Div(className="table_features", children=[
                                                            dcc.Loading(
                                                                dbc.Table.from_dataframe(df=
                                                                    pd.DataFrame({
                                                                        "Feature":[],
                                                                        "Number of models":[]
                                                                    })
                                                                ,
                                                                id="overview_table",
                                                                striped=True, bordered=True,
                                                                hover=True),
                                                                # dash_table.DataTable(
                                                                #     id="overview_table",
                                                                #     columns=[{"name": i, "id": i} for i in ["Feature", "Number of models"]],
                                                                #     style_table={
                                                                #         'maxHeight': '300px',
                                                                #         'overflowY': 'scroll'
                                                                #     },
                                                                #     style_as_list_view=True,
                                                                #     style_cell={
                                                                #         'padding': '5px',
                                                                #         "textAlign": "center"
                                                                #     },
                                                                # )
                                                            ),
                                                        ]),
                                                        html.Div(className="umap_plot_and_title", children=[
                                                            html.Div(className="title_and_help",
                                                                     children=[html.H6("Umap"),
                                                                               dbc.Button("[?]", className="text-muted",
                                                                                          id="help_umapPlot"),
                                                                               dbc.Popover(children=[
                                                                                   dbc.PopoverBody(
                                                                                       "Blablabla wout wout")
                                                                               ],
                                                                                   id="pop_help_umapPlot",
                                                                                   is_open=False,
                                                                                   target="help_umapPlot")
                                                                               ]
                                                            ),
                                                            dcc.Loading(
                                                                dcc.Graph(id="umap_overview"),
                                                                type="circle")
                                                        ])
                                                    ]
                                                    )
                                                ]
                                            ),
                                            dbc.Tab(className="sub_tab",
                                                label="Specific Results",
                                                children=[
                                                    html.Div(className="fig_group", children=[
                                                        html.Div(className="fig_group_col", children=[
                                                            html.Div(className="", children=[
                                                                html.H6("Experiment number"),
                                                                dbc.Select(id="experiment_dropdown",
                                                                           className="form_select_large",
                                                                           options=[{"label": i, "value": i} for i in
                                                                                      range(LEARN_CONFIG["Nsplit"])],
                                                                           value="0"
                                                                ),
                                                                html.H6("Show QCs"),
                                                                dbc.Checklist(id="show_qc_checklist",
                                                                              # switch=True,
                                                                              options=[
                                                                                  # Not sure how to label these
                                                                                  {"label": "QC all run", "value": "true"}]
                                                                              ),
                                                                dbc.Button("Update", color="primary",id="update_specific_results_button",
                                                                            className="custom_buttons", n_clicks=0),
                                                                html.Div(id="output_button_update_specific_results"),
                                                            ]
                                                            ),
                                                            html.Div(className="",
                                                                     children=[
                                                                         html.H6("Experiment metrics")])
                                                        ]),
                                                        # PCA
                                                        html.Div(className="pca_plot_and_title", children=[
                                                            html.Div(className="title_and_help",
                                                                     children=[html.H6("PCA", id="PCA_title"),
                                                                               dbc.Button("[?]", className="text-muted",
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
                                                    ]),
                                                    html.Div(className="fig_group", children=[
                                                        html.Div(className="bxplot_plot_select_and_title", children=[
                                                            html.Div(className="title_and_help",
                                                                     children=[html.H6("Metabolite Level"),
                                                                               dbc.Button("[?]", className="text-muted",
                                                                                          id="help_BxPlot"),
                                                                               dbc.Popover(children=[
                                                                                   dbc.PopoverBody(
                                                                                       "Blablabla wout wout")
                                                                               ],
                                                                                   id="pop_help_BxPlot",
                                                                                   is_open=False,
                                                                                   target="help_BxPlot")
                                                                               ]
                                                            ),
                                                            html.Div(id="metrics_table",
                                                                     style={"margin": "auto", "display": "flex",
                                                                            "justify-content": "center"}),
                                                            html.Div(id="metabolite_dropdown_container", children=[
                                                                dbc.Select(id="metabolite_dropdown",
                                                                           className="form_select_large",
                                                                           options=[],
                                                                           )
                                                            ]),
                                                            dcc.Graph(id="metabo_boxplot",
                                                                      figure=go.Figure(
                                                                          data=[go.Box(
                                                                              x=[1, 2, 3, 4, 5, 5, 5, 5, 5, 5, 5, 6, 7,
                                                                                 8]),
                                                                                go.Box(
                                                                                    x=[10, 10, 10, 10, 9, 9, 9, 9, 9, 7,
                                                                                       8, 5, 12, 12, 15])],
                                                                          layout=go.Layout(
                                                                              paper_bgcolor='rgba(0,0,0,0)',
                                                                              plot_bgcolor='rgba(0,0,0,0)')
                                                                      )
                                                            )

                                                        ]),


                                                        html.Div(className="heatmap_plot_and_title", children=[
                                                            html.Div(className="title_and_help",
                                                                     children=[html.H6("Heatmap",id="heatmap_title"),
                                                                               dbc.Button("[?]", className="text-muted",
                                                                                          id="help_heatmapPlot"),
                                                                               dbc.Popover(children=[
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
                                                    ]),
                                                ]
                                            ),
                                        ]),

                                    ]),
                        ]),
                        #################
                        # Interpret tab #
                        #################
                        dbc.Tab(className="global_tab",
                             # tab_style={"margin-left": "auto"},
                             label="Model Interpretation", children=[
                             html.P("A tab to allow model interpretation with model-agnostic methods.")
                         ]),
                     ])
        ]),
    ])


app.layout = layout()


                                             ###############################
# -------------------------------------------#            SPLITS           #
                                             ###############################
@app.callback(
    [Output("div_pair_pn", "style"),
     Output("div_pair_12", "style")],
    [Input("in_pairing_pos_neg", "value"),
     Input("in_pairing_samples", "value")]
)
def pairing_show_hide_name_fields(pair_pn, pair_12):
    if pair_pn == [0] and pair_12 == [0]:
        return {"display": "block"}, {"display": "block"}
    elif pair_pn == [0] and pair_12 != [0]:
        return {"display": "block"}, {"display": "none"}
    elif pair_pn != [0] and pair_12 == [0]:
        return {"display": "none"}, {"display": "block"}
    else:
        return {"display": "none"}, {"display": "none"}


@app.callback([Output("in_target_col_name", "options"),
               Output("in_ID_col_name", "options"),
               Output("output_in_case_of_error_in_path_to_metadata", "children")],
              [Input("in_path_to_metadata", "value")])
def get_metadata_cols_names_to_choose_from(path_value):
    options_list = ["None"]
    print(options_list)
    if path_value is None:
        return dash.no_update
    elif path_value.split(".")[-1] == "csv":
        df_metadata = pd.read_csv(path_value)
    elif "xls" in path_value.split(".")[-1] or "od" in path_value.split(".")[-1]:
        df_metadata = pd.read_excel(path_value)
    else:
        return [], [], "There is a problem, the format of your metadata file might not be supported. You need to give either a .csv, .xlsX or .odX (where X replace variation of format). Ex: file.xlsx, file.odt"

    options_list.extend(list(df_metadata.columns))
    print(options_list)
    return [{'label': col, 'value': col} for col in options_list], [{'label': col, 'value': col} for col in options_list], ""


@app.callback(
    Output("define_classes_desgn_exp", "children"),
    [Input("in_classification_type", "value")]
)
def define_classes_for_experiment_design(t):
    """
    if the classification type is binary (0), certain options will be available
    if it is multiclass (1), other options wil be shown
    :param t:
    :return:
    """
    if t == 0:
        return [
                html.Div(className="title_and_form_mini", children=[
                    dbc.Form(children=[
                        dbc.Col(children=[
                            dbc.FormGroup(
                                [
                                    dbc.Label("Label 1"),
                                    dbc.Input(id="class1_name",
                                              placeholder="Enter name",
                                              debounce=True,
                                              className="form_input_text"),

                                ],
                                className="form_field"
                            ),
                            dbc.FormGroup(
                                [
                                    dbc.Label("Class(es)"),
                                    dbc.Checklist(
                                        id="possible_groups_for_class1")
                                ]
                            )
                        ])
                    ])
                ]),
                html.Div(className="title_and_form_mini", children=[
                    dbc.Form(children=[
                        dbc.Col(children=[
                            dbc.FormGroup(
                                [
                                    dbc.Label("Label 2"),
                                    dbc.Input(id="class2_name",
                                              placeholder="Enter name",
                                              debounce=True,
                                              className="form_input_text"),

                                ],
                                className="form_field"
                            ),
                            dbc.FormGroup(
                                [
                                    dbc.Label("Class(es)"),
                                    dbc.Checklist(
                                        id="possible_groups_for_class2")
                                ]
                            )
                        ])
                    ])
                ])
        ]


@app.callback(
    [Output("possible_groups_for_class1", "options"),
     Output("possible_groups_for_class2", "options"),
     Output("output_btn_add_desgn_exp", "children")],
    [Input("in_target_col_name", "value")],
    [State("in_path_to_metadata", "value")]
)
def update_possible_classes_exp_design(target_col, path_metadata):
    if target_col != 0:
        print("target_col value is : {}".format(target_col))
        if path_metadata is None or path_metadata == "":
            return [], [], "There is a problem, check if there is a file in the 'Path to metadata file' field."
        elif path_metadata.split(".")[-1] == "csv":
            df_metadata = pd.read_csv(path_metadata)
        elif "xls" in path_metadata.split(".")[-1] or "od" in path_metadata.split(".")[-1]:
            df_metadata = pd.read_excel(path_metadata)
        else:
            return [], [], "There is a problem, the format of your metadata file might not be supported. You need to give either a .csv, .xlsY or .odY (where Y replace variation of format). Ex: file.xlsx, file.odt"

        possible_targets = list(set(list(df_metadata[target_col])))
        return [{'label': i, 'value': i} for i in possible_targets], [{'label': i, 'value': i} for i in possible_targets], ""
    else:
        return [], [], ""


@app.callback(
    [Output("class1_name", "value"),
     Output("possible_groups_for_class1", "value"),
     Output("class2_name", "value"),
     Output("possible_groups_for_class2", "value")],
    [Input("btn_add_design_exp", "n_clicks")],
    [State("class1_name", "value"),
     State("possible_groups_for_class1", "value"),
     State("class2_name", "value"),
     State("possible_groups_for_class2", "value")]
)
def add_n_reset_classes_exp_design(n, c1, g1, c2, g2):
    """
    When the "Add" button is pushed on the interface, the values for the new experimental design are saved to a file.
    Then, the fields are cleared so the user can input another design if desired.
    :param n:
    :param c1:
    :param g1:
    :param c2:
    :param g2:
    :return:
    """
    if n >= 1:
        new_desgn_name = "{}_vs_{}".format(c1, c2)
        new_desgn_classes = {c1: g1, c2: g2}

        Experiment_desgn_file = "temp_exp_designs.json"

        if not os.path.exists(Experiment_desgn_file):
            with open(Experiment_desgn_file, "w+") as design_file:
                data = {}
                json.dump(data, design_file)

        with open(Experiment_desgn_file, "r+") as design_file:
            data = json.load(design_file)

            data[new_desgn_name] = new_desgn_classes

            design_file.seek(0)
            json.dump(data, design_file)
            design_file.truncate()
        return "", 0, "", 0
    else:
        return dash.no_update

@app.callback(
    Output("collapse_preprocessing", "is_open"),
    [Input("collapse_preprocessing_button", "n_clicks")],
    [State("collapse_preprocessing", "is_open")],
)
def toggle_collapse_preprocessing(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output('output_button_split_file', 'children'),
    [Input('split_dataset_button', 'n_clicks')],
    [State("name_splits_batch", "value"),
     State("in_use_raw", "value"),
     State('in_nbr_splits', 'value'),
     State('in_nbr_processes', 'value'),
     State("path_to_data_file", "value"),
     State('in_peak_threshold_value', 'value'),
     State('in_percent_samples_in_test', 'value'),
     State('in_autoOptimize_value', 'value'),
     State('in_path_to_metadata', 'value'),
     State('in_ID_col_name', 'value'),
     State('in_target_col_name', 'value'),
     State("in_type_of_data", "value"),
     State("in_peak_picking", "value"),
     State("in_alignment", "value"),
     State("in_normalization", "value"),
     State("in_pairing_pos_neg", "value"),
     State("distinct_id_pos_samples", "value"),
     State("distinct_id_neg_samples", "value"),
     State("in_pairing_samples", "value"),
     State("distinct_id_1_samples", "value"),
     State("distinct_id_2_samples", "value"),
     ]
)
def saving_params_of_splits_batch(n, name_of_the_file, use_raw, nbr_splits, nbr_processes, path_data_files,
                                        peakT, percent_in_test, autoOpt, path_to_metadata, ID_col_name, targets_col_name,
                                        type_of_processing, peak_pick, align, normalize, pair_pn, pair_id_pos,
                                        pair_id_neg, pair_12, pair_id_1, pair_id_2):
    """
    Create the file (json) which will contains all info about the split creation / data experiment.
    """
    if n >= 1:
        date_time = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

        # Load the asked experiment design
        with open("temp_exp_designs.json", "r+") as design_file:
            dict_exp_desgn = json.load(design_file)

        # Load metadata file as dataframe
        if path_to_metadata.split(".")[-1] == "csv":
            df_metadata = pd.read_csv(path_to_metadata)
        elif "xls" in path_to_metadata.split(".")[-1] or "od" in path_to_metadata.split(".")[-1]:
            df_metadata = pd.read_excel(path_to_metadata)
        else:
            print("There is a problem, the format of your metadata file might not be supported. You need to give either a .csv, .xlsY or .odY (where Y replace variation of format). Ex: file.xlsx, file.odt")

        # Prepare data for splits creation and handle pairing
        uniq_ID = [str(i) for i in list(df_metadata[ID_col_name])]
        #TODO: prob de coherence entre labels du fichier metadata et ceux direct du fichier de donnees
        targets = list(df_metadata[targets_col_name])

        # Convert the data to fit the format
        f = DataFormat(path_data_files, use_raw)
        features_info, data, labels, sample_names = f.convert()

        # Handle paired samples if need be
        if pair_pn == [0]:
            pairing_pn = [pair_id_pos, pair_id_neg]
        else:
            pairing_pn = "no"

        if pair_12 == [0]:
            pairing_12 = [pair_id_1, pair_id_2]
        else:
            pairing_12 = "no"


        #TODO: revoir pcq gestion avec fichiers (lcs) donc pas adapter pour matrices csv LCMS
        # Do the pairing, all handled by a class : SamplesPairing
        # and the splits are also created at the same time
        pairing = SamplesPairing([pairing_pn, pairing_12], sample_names, labels, uniq_ID, percent_in_test, nbr_splits)
        pairing.split()
        splits_dict = pairing.dict_splits

        # ---------- !!!!!! most recent : désigner les samples par leur nom, mettre un ID unique = trop complexe a gérer

        # Organizing data to write to config file
        df_metadata = df_metadata.to_dict("list")
        opt_process = [peak_pick, align, normalize]

        split_batch_info = {
            "Date_of_creation": date_time,
            "Type_of_processing": type_of_processing,
            "Options_of_processing": opt_process,
            "Nbr_splits": nbr_splits,
            "Nbr_processes": nbr_processes,
            "Proportion_in_test": percent_in_test,
            "Peak_threshold": peakT,
            "AutoOptimize_nbr": autoOpt,
            "Experimental_designs": dict_exp_desgn,
            "Pairing_pos_neg": pairing_pn,
            "Pairing_other": pairing_12,
            "Data_matrix": data.to_json(),
            "Splits": splits_dict,
            "Metadata": df_metadata,
            "Features_info": features_info.to_json(),
        }

        # Writing to config file
        with open(name_of_the_file, "w+") as history_file:
            json.dump(split_batch_info, history_file)
        return "The parameters file is created, the splits's creation should start shortly..."
    else:
        return dash.no_update


                                             ################################
# -------------------------------------------#       Machine Learning       #
                                             ################################

@app.callback(
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
    sklearn_algo_file = "algo_sklearn.json"

    if n >= 1:
        new_algo_name = name_new
        new_algo_params = {"function": name_new, "ParamGrid": {name_param: values_param}, "importing": import_new}

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


@app.callback(
    Output("output_button_ml", "children"),
    [Input("start_learning_button", "n_clicks")],
    [State("in_algo_ML", "value"),
     State("name_splits_config", "value"),
     State("in_nbr_CV_folds", "value"),
     State("in_nbr_processes", "value")]
)
def start_machine_learning(n, selected_algos, split_config_file, cv_folds, nbr_process):
    if n >= 1:
        with open("algo_sklearn.json", "r") as algo_file:
            algo_list = json.load(algo_file)

        with open(split_config_file, "r") as conf_file:
            splits_config = json.load(conf_file)

        print("Splits_dict 1er element = {}".format(splits_config["Splits"][list(splits_config["Splits"].keys())[0]]))
        print("---")
        print("Data matrix type = {}".format(type(pd.read_json(splits_config["Data_matrix"]))))
        print("Data matrix 2 first lines = {}".format(pd.read_json(splits_config["Data_matrix"]).iloc[:2, :5]))

        # get all files : X_train files [0] and X_test files [1]
        #all_data_files = splits_config["Splits"]["split0"][0] + splits_config["Splits"]["split0"][1]

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






                                                   ################################
# -------------------------------------------------#            RESULTS           #
                                                   ################################




@app.callback(
    Output("pop_help_accPlot", "is_open"),
    [Input("help_accPlot", "n_clicks")],
    [State("pop_help_accPlot", "is_open")],
)
def toggle_popover(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
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

@app.callback(
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


@app.callback(
    Output("loading-output-1", "children"),
    [Input("custom_big_tabs", "active_tab")]
)
def input_triggers_spinner(value):
    time.sleep(1)
    return


@app.callback(
    Output("view_info", "children"),
    [Input("custom_big_tabs", "active_tab")]
)
def get_experiment_statistics(active):
    if active == "tab-3":
        with open("testest", "r") as conf_file:
            splits_config = json.load(conf_file)

        splits_dict = splits_config["Splits"]
        nbr_in_train = len(splits_dict["split0"][0])
        nbr_in_test = len(splits_dict["split0"][1])
        nbr_tot = nbr_in_train + nbr_in_test
        classes_train = splits_dict["split0"][2]
        classes_tot = classes_train.extend(splits_dict["split0"][3])
        count_per_class = Counter(classes_tot)

        row1 = html.Tr([html.Td("Total number of samples"), html.Td(str(nbr_tot))])
        row2 = html.Tr([html.Td("Number of samples in train"), html.Td(str(nbr_in_train))])
        row3 = html.Tr([html.Td("Number of samples in test"), html.Td(str(nbr_in_test))])
        # row4 = html.Tr([html.Td(list(count_per_class.keys())[0]), html.Td("Astra")])

        table_body = [html.Tbody([row1, row2, row3])]
        table = dbc.Table(table_body, id="table_exp_info", borderless=True, hover=True)

        return table
    else:
        return dash.no_update


@app.callback(
    Output("accuracy_overview", "figure"),
    [Input("load_ML_results_button", "n_clicks")],
    [State("ml_dropdown", "value"),
     State("design_dropdown", "value")]
)
def generates_accuracyPlot_global(n_clicks, ml_dropdown, design_dropdown):
    if n_clicks >= 1:
        rez_files = glob.glob(os.path.join("Results", design_dropdown + "_*_" + ml_dropdown + ".pkl"))

        acc_train = []
        acc_test = []
        for file in rez_files:
            with open(file, "rb") as f:
                GS_rez = pkl.load(f)
                train_predict = pkl.load(f)
                test_predict = pkl.load(f)
                train_targets = pkl.load(f)
                test_targets = pkl.load(f)

            acc_train.append(accuracy_score(train_targets, train_predict)*100)
            acc_test.append(accuracy_score(test_targets, test_predict)*100)

        acc_fig = go.Figure()
        x_axis = [str(i) for i in range(len(acc_train))]

        acc_fig.add_trace(
            go.Scatter(
                x=x_axis,
                y=acc_train,
                mode="lines+markers",
                name="Train accuracies"
            )
        )

        acc_fig.add_trace(
            go.Scatter(
                x=x_axis,
                y=acc_test,
                mode="lines+markers",
                marker_symbol="diamond",
                name="Test accuracies"
            )
        )

        acc_fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Splits",
            yaxis_title="Accuracy (%)"
        )

        return acc_fig
    else:
        return dash.no_update




@app.callback(
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

        print(np.array(train_df).shape)
        train_df = filter_cluster(train_df, threshold=1.0)
        print(np.array(train_df).shape)
        embedding = reducer.fit_transform(train_df)

        trace_train = go.Scatter(
            x=embedding[:, 0],
            y=embedding[:, 1],
            mode="markers",
            text=np.array(train_df.index)
        )
        fig_umap = go.Figure(data=[trace_train],
                             layout=go.Layout(
                                 paper_bgcolor='rgba(0,0,0,0)',
                                 plot_bgcolor='rgba(0,0,0,0)')
                             )
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

        return fig_acc, df, fig_umap, ""  # .to_dict("records")

    else:
        return dash.no_update

@app.callback(
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





                                             #############################
# -------------------------------------------#            ELSE           #
                                             #############################


# @app.callback(Output('output_button_split', 'children'),
#               [Input('split_dataset_button', 'n_clicks')],
#               [State('in_nbr_splits', 'value'),
#                State('in_nbr_processes', 'value'),
#                State('path_output_splits', 'value'),
#                State('in_peak_threshold_value', 'value'),
#                State('in_percent_samples_in_test', 'value'),
#                State('in_autoOptimize_value', 'value'),
#                State('in_path_to_metadata', 'value'),
#                State('in_ID_col_name', 'value'),
#                State('in_target_col_name', 'value')],
#               )
# def start_splits_creation(n_clicks,  nbr_splits, nbr_processes, o_path, peakThreshold, percentTest, autoOpt,
#                           path_metadata, ID_col, target_col):
#     if n_clicks >= 1:
#
#         try:
#             files_count_splits = np.array(glob.glob(o_path + "*.txt"))
#             for f in files_count_splits:
#                 os.remove(f)
#         except:
#             pass
#
#         if o_path == '':
#             o_path = "./"
#         script_name = "script_create_splits.py"
#         os.system(
#             "python3 {} -i {} -o {} -ns {} -np {} -peakT {} -nbrTest {} -autoOpt {} -mfile {} -idcol {} -tcol {}".format(
#                 script_name, path_to_lcs, o_path, nbr_splits, nbr_processes, peakThreshold, percentTest, autoOpt,
#                 path_metadata, ID_col, target_col))
#
#         return "0"
#     else:
#         return dash.no_update




@app.callback(
    Output("interval_div", "children"),
    [Input('split_dataset_button', 'n_clicks')]
)
def start_progress_bar_intervals_updating(n_clicks):
    if n_clicks >= 1:
        return dcc.Interval(id="interval", interval=60000, n_intervals=0)
    else:
        return dash.no_update

@app.callback(
    [Output("interval", "disabled"),
     Output("progress", "value"),
     Output("progress", "children")],
    [Input("interval", "n_intervals")],
    [State('in_nbr_splits', 'value'),
     State("progress", "value"),
     State('path_output_splits', 'value')]
)
def update_progress_bar(n, nbr_splits_total, progress_done, path_output_splits):
    if progress_done == 100:
        return True, progress_done, f"{progress_done} %" if progress_done >= 5 else ""
    else:
        nbr_split_created = len(glob.glob("{}/*".format(path_output_splits)))
        new_progress = int((nbr_split_created/int(nbr_splits_total))*100)
        return False, new_progress, f"{new_progress} %" if new_progress >= 5 else ""




def get_experiment_statistics(y_true_train, y_pred_train, y_true_test, y_pred_test):
    # TODO: Increase margins bottom.
    table = []
    table_style = {"padding": "12px 55px", "text-align": "left"}
    table.append(html.Tr([html.Th("Metric", style=table_style), html.Th("Train"), html.Th("Test")]))
    for stat in STATISTICS:
        metric_value_train = STATISTICS[stat](y_true_train, y_pred_train)
        metric_value_test = STATISTICS[stat](y_true_test, y_pred_test)
        if isinstance(metric_value_test, float):
            metric_value_test = "{:0.2f}".format(metric_value_test)
        if isinstance(metric_value_train, float):
            metric_value_train = "{:0.2f}".format(metric_value_train)
        #new_div = html.Div("{}: {}, {}".format(stat, metric_value_train, metric_value_test))
        table.append(html.Tr([html.Td(stat), 
            html.Td(metric_value_train), 
            html.Td(metric_value_test)]
        ))
    return html.Table(table)
    #return children

# @app.callback(
#     [Output("accuracy_overview", "figure"),
#     Output("overview_table", "children"),
#     Output("umap_overview", "figure"),
#     Output("output_button_load_ML_results", "children")],
#     [Input("load_ML_results_button", "n_clicks")],
#     [State("ml_dropdown", "value"),
#     State("design_dropdown", "value")]
# )
# def show_global_view(n_clicks, ml_dropdown, design_dropdown):
#     if n_clicks >= 1:
#         print("Updating global accuracy plot")
#         splits_name = []
#         split_train_accuracy = []
#         split_test_accuracy = []
#
#         features = []
#         data_matrix_filename = os.path.join("Results", design_dropdown + "_0_" + ml_dropdown + ".pkl")
#         with open(data_matrix_filename, "rb") as fi:
#             train_df = pkl.load(fi)  #, encoding='bytes'
#             train_targets = pkl.load(fi)  #, encoding='latin1'
#             test_df = pkl.load(fi)  #, encoding='latin1'
#             test_targets = pkl.load(fi)  #, encoding='latin1'
#
#         cols = ["a"] * len(train_df[0])
#         train_df = pd.DataFrame(train_df, columns=cols)
#
#         reducer = umap.UMAP()
#
#         def filter_cluster(df, threshold=0.5):
#             """
#             threshold : (proportion) minimum of non-zero values in a line to consider keeping this line
#             for example -> threshold = 0.6 means it will keep only the lines where there is at least 60% of non-zero values
#             """
#             df = df.T
#             nbr_col = len(df.columns.to_list())
#             print(nbr_col)
#             print((df.astype(bool).sum(axis=0)).shape)
#             df_filtered = df.loc[df.astype(bool).sum(axis=1) >= nbr_col*threshold]
#             return df_filtered.T
#
#         print(np.array(train_df).shape)
#         train_df = filter_cluster(train_df, threshold=1.0)
#         print(np.array(train_df).shape)
#         embedding = reducer.fit_transform(train_df)
#
#         trace_train = go.Scatter(
#             x=embedding[:, 0],
#             y=embedding[:, 1],
#             mode="markers",
#             text=np.array(train_df.index)
#         )
#         fig_umap = go.Figure(data=[trace_train],
#                         layout=go.Layout(
#                             paper_bgcolor='rgba(0,0,0,0)',
#                             plot_bgcolor='rgba(0,0,0,0)')
#                         )
#         # return(fig, dash.no_update)
#
#
#
#         for model_filename in glob.glob(os.path.join("Results", design_dropdown+"_*_"+ml_dropdown+"*")):
#             with open(model_filename, "rb") as fi:
#                 gc = pkl.load(fi)
#                 print(gc.best_estimator_.classes_)
#                 train_predict = pkl.load(fi)
#                 test_predict = pkl.load(fi)
#
#             data_matrix_filename = os.path.join("Splits", design_dropdown + "_" + model_filename.split("_")[1])
#             with open(data_matrix_filename, "rb") as fi:
#                 train_df = pkl.load(fi)
#                 train_targets = pkl.load(fi)
#                 test_df = pkl.load(fi)
#                 test_targets = pkl.load(fi)
#
#             splits_name.append(model_filename.split("_")[1])
#             split_train_accuracy.append(accuracy_score(y_true=train_targets, y_pred = train_predict))
#             split_test_accuracy.append(accuracy_score(y_true=test_targets, y_pred=test_predict))
#
#             if isinstance(gc.best_estimator_, RandomForestClassifier) or \
#                 isinstance(gc.best_estimator_, DecisionTreeClassifier):
#                 features_importance = gc.best_estimator_.feature_importances_
#
#             zipped = zip(features_importance, train_df.columns)
#             zipped = sorted(zipped, key = lambda t:t[0])
#
#             [features.append(i[1]) for i in zipped if np.abs(i[0]) > 0.0]
#
#         features_count = Counter(features)
#
#         #table = []
#         #table_style = {"padding": "12px 55px", "text-align": "left"}
#         #table.append(html.Tr([html.Th("Feature", style=table_style), html.Th("Number of models")]))
#         #for f in features_count.most_common():
#         #    table.append(html.Tr([html.Td(f[0]), html.Td(f[1])]))
#         features_column = []
#         n_models_column = []
#         for f in features_count.most_common():
#             features_column.append(f[0])
#             n_models_column.append(f[1])
#
#         df = pd.DataFrame()
#         df["Feature"] = features_column
#         df["Number of models"] = n_models_column
#
#         trace_train = go.Scatter(
#             y=split_train_accuracy,
#             name="Train accuracy"
#         )
#         trace_test = go.Scatter(
#             y=split_test_accuracy,
#             name="Test accuracy"
#         )
#         fig_acc = go.Figure(data=[trace_train, trace_test])
#         print("Number of items:{}".format(len(train_df.columns)))
#
#         print("df : {}".format(df))
#         df = pd.DataFrame({
#                             "Feature":[],
#                             "Number of models":[]
#                         })
#
#         return fig_acc, df, fig_umap, ""  #.to_dict("records")
#
#     else:
#         return dash.no_update
#
#
# @app.callback(
#     Output("global_metrics", "children"),
#     [Input("compute_global_metrics", "n_clicks"),
#     Input("ml_dropdown", "value"),
#     Input("design_dropdown", "value")]
# )
# def compute_global_metrics(n_clicks, ml_algo, exp_design):
#     if n_clicks is None or n_clicks == 0:
#         return dash.no_update
#     if dash.callback_context.triggered[0]['prop_id'].split('.')[0] != "compute_global_metrics":
#         return ""
#     data_matrix_file_list = glob.glob(os.path.join("Splits", "{}_*".format(exp_design)))
#     metrics_results_train =  {i:[] for i in STATISTICS}
#     metrics_results_test =  {i:[] for i in STATISTICS}
#
#     for data_matrix_filename in data_matrix_file_list:
#         split_number = data_matrix_filename.split("_")[-1]
#         model_filename = os.path.join("Results",
#             "{}_{}_{}.pkl".format(exp_design, split_number, ml_algo))
#
#         with open(data_matrix_filename, "rb") as fi:
#             train_df = pkl.load(fi, encoding="latin1")
#             train_targets = pkl.load(fi, encoding="latin1")
#             test_df = pkl.load(fi, encoding="latin1")
#             test_targets = pkl.load(fi, encoding="latin1")
#
#         with open(model_filename, "rb") as fi:
#             gc = pkl.load(fi, encoding="latin1")
#             print(gc.best_estimator_.classes_)
#             train_predict = pkl.load(fi, encoding="latin1")
#             test_predict = pkl.load(fi, encoding="latin1")
#
#         for stat in STATISTICS:
#             metrics_results_train[stat].append(
#                 STATISTICS[stat](train_targets, train_predict)
#             )
#             metrics_results_test[stat].append(
#                 STATISTICS[stat](test_targets, test_predict)
#             )
#     table = []
#     table_style = {"padding": "12px 55px", "text-align": "left"}
#     table.append(html.Tr([html.Th("Metric", style=table_style), html.Th("Train"), html.Th("Test")]))
#     for stat in STATISTICS:
#         print(stat)
#         train_average = np.average(metrics_results_train[stat])
#         test_average = np.average(metrics_results_test[stat])
#         train_std = np.std(metrics_results_train[stat])
#         test_std = np.std(metrics_results_test[stat])
#         print(train_average, train_std)
#         table.append(html.Tr([html.Td(stat),
#             html.Td("{:0.2f} ({:0.2f})".format(train_average, train_std)),
#             html.Td("{:0.2f} ({:0.2f})".format(test_average, test_std))]
#         ))
#     return html.Table(table)
#


@app.callback(
    Output("metabo_boxplot", "figure"),
    [Input("metabolite_dropdown", "value")],
    [State("design_dropdown", "value"),
    State("experiment_dropdown", "value")]
)
def update_boxplot_metabolite(metabolite_name, exp_design, ml_exp_number):
    data_matrix_filename = os.path.join("Splits",
        "{}_{}".format(exp_design, ml_exp_number))
    
    # Load data matrix
    with open(data_matrix_filename, "rb") as fi:
        train_df = pkl.load(fi)
        train_targets = pkl.load(fi)
        test_df = pkl.load(fi)
        test_targets = pkl.load(fi)

    merged_df = train_df.append([test_df])
    merged_targets = np.concatenate([train_targets,test_targets])
    if metabolite_name is None:
        return dash.no_update
    selected_metabo_data = np.array(merged_df[metabolite_name])

    box_traces = []
    for i in set(merged_targets):
        box_traces.append(go.Box(
            x=selected_metabo_data[np.array(merged_targets) == i],
            name=i)
        )
    layout = go.Layout(title="Abunce level of the selected metabolite between classes",
                       paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)'
                       )

    return go.Figure(data=box_traces, layout=layout)



@app.callback(
    [Output("PCA", "figure"),
    Output("PCA_title", "children"),
    Output("metabolite_dropdown", "options"),
    Output("metabolite_dropdown", "value"),
    Output("heatmap", "src"),
    Output("heatmap_title", "children"),
    Output("metrics_table", "children"),
    # Output("view_info", "children")
     ],
    [Input("load_ML_results_button", "n_clicks"),
     Input("update_specific_results_button", "n_clicks")
     ],
    [State("design_dropdown", "value"),
    State("ml_dropdown", "value"),
    State("experiment_dropdown", "value"),
    State("show_qc_checklist", "value")]
)
def update_core(n_click_general, n_clicks_specific, exp_design, ml_exp_name, ml_exp_number, show_qc):
    if n_click_general >= 1 or n_clicks_specific >= 1:
        print("-----updating core")
        model_filename = os.path.join("Results",
            "{}_{}_{}.pkl".format(exp_design, ml_exp_number, ml_exp_name))

        data_matrix_filename = os.path.join("Splits",
            "{}_{}".format(exp_design, ml_exp_number))

        # Load GridSearch
        with open(model_filename, "rb") as fi:
            gc = pkl.load(fi)
            train_predict = pkl.load(fi)
            test_predict = pkl.load(fi)

        # Load data matrix
        with open(data_matrix_filename, "rb") as fi:
            train_df = pkl.load(fi, encoding="latin1")
            train_targets = pkl.load(fi, encoding="latin1")
            test_df = pkl.load(fi, encoding="latin1")
            test_targets = pkl.load(fi, encoding="latin1")

        cols = ["a"] * len(train_df[0])
        train_df = pd.DataFrame(train_df, columns=cols)

        cols2 = ["a"] * len(test_df[0])
        test_df = pd.DataFrame(test_df, columns=cols2)

        # Prepare View Info

        view_info_children = []
        view_info_children.append(html.Div("{} samples in the dataset".format(len(train_targets) + len(test_targets))))
        view_info_children.append(html.Div("{} samples in the training set".format(len(train_targets))))
        #for c in set(train_targets):
        #    view_info_children.append(html.Div("    {} are {}".format(np.sum(np.array(train_targets==c)), c)))
        view_info_children.append(html.Div("{} samples in the testing set".format( len(test_targets))))
        #for c in set(test_targets):
        #    view_info_children.append(html.Div("    {} are {}".format(np.sum(np.array(test_targets==c), c))))

        # Compute Metrics table
        metric_table = get_experiment_statistics(train_targets, train_predict, \
            test_targets, test_predict)

        # Filter important features
        if isinstance(gc.best_estimator_, RandomForestClassifier) or \
                isinstance(gc.best_estimator_, DecisionTreeClassifier):
            features_importance = gc.best_estimator_.feature_importances_
        else:
            raise ValueError("Check code and define features extraction process.")

        zipped = zip(features_importance, train_df.columns)
        zipped = sorted(zipped, key = lambda t:t[0])

        if np.sum(features_importance > 0.0) < NUMBER_METABO_TO_KEEP:
            important_index = [i[1] for i in zipped[-1*np.sum(features_importance > 0.0):]]
        else:
            important_index = [i[1] for i in zipped[-1*NUMBER_METABO_TO_KEEP:]]

        train_df_filtered = train_df[important_index]
        test_df_filtered = test_df[important_index]


        # Compute PCA
        merged_df = train_df_filtered.append([test_df_filtered])

        std_clf = make_pipeline(StandardScaler(), PCA(n_components=2))
        #pca_merged = pca.fit_transform(merged_df)
        std_clf.fit(train_df_filtered)
        train_pca_transformed = std_clf.transform(train_df_filtered)
        test_pca_transformed = std_clf.transform(test_df_filtered)

        # Create PCA plot
        print(train_targets)
        print(test_targets)
        merged_targets = np.concatenate([train_targets,test_targets])

        train_targets = np.array(train_targets)
        test_targets = np.array(test_targets)

        pca_traces = []
        for c in gc.classes_:
            trace = go.Scatter(
                x=train_pca_transformed[train_targets==c, 0],
                y=train_pca_transformed[train_targets==c, 1],
                name="{} training".format(c),
                mode="markers"
            )
            pca_traces.append(trace)
            trace = go.Scatter(
                x=test_pca_transformed[test_targets==c, 0],
                y=test_pca_transformed[test_targets==c, 1],
                name="{} testing".format(c),
                mode="markers"
            )
            pca_traces.append(trace)
        layout = go.Layout(xaxis={"title":"{:0.2f}%".format(std_clf[1].explained_variance_ratio_[0]*100)},
                           yaxis={"title":"{:0.2f}%".format(std_clf[1].explained_variance_ratio_[1]*100)},
                           paper_bgcolor='rgba(0,0,0,0)',
                           plot_bgcolor='rgba(0,0,0,0)'
                           )
        figure_pca = go.Figure(data=pca_traces, layout=layout)
        pca_title = "PCA plot using {} metabolites selected using the {} algorithm on split {}".format(
            train_df_filtered.shape[1], ml_exp_name, ml_exp_number)

        # Create Metabolite dropdown
        metabolite_dropdown = [{"label": i, "value": i} for i in important_index]
        selected_metabolite_value = important_index[0]

        # Create heatmap using merged DF
        heatmap = get_static_heatmap_plot(StandardScaler().fit_transform(merged_df), \
            merged_df.columns.values, merged_df.index, merged_targets)
        heatmap_title = "Heat-map of {} metabolite normalized abuncance across the different samples".format(
            train_df_filtered.shape[1])
        #Return values
        return figure_pca, pca_title, metabolite_dropdown, selected_metabolite_value, \
            heatmap, heatmap_title, metric_table, view_info_children
    else:
        return dash.no_update


def get_static_heatmap_plot(NpArray, Label_X, Label_Y, targets):
    target_colors = dict(zip(set(targets), sns.color_palette("Set2")))
    print(target_colors)
    row_colors = [target_colors[i] for i in targets]
    heatmap = sns.clustermap(pd.DataFrame(NpArray, columns=Label_X, index=Label_Y),
         row_colors=row_colors, cmap="RdBu_r")
    fig = heatmap.fig
    buf = io.BytesIO() # in-memory files
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("utf8") # encode to html elements
    #plt.close()
    return "data:image/png;base64,{}".format(data)

def get_heatmap_plot(NpArray, Label_X, Label_Y):
    component = dash_bio.Clustergram(
        hidden_labels=['row'],
        color_threshold={'row': 150, 'col': 700},
        data=NpArray,
        column_labels=list(Label_X),
        width=700,
        height=800,
        row_labels=list(Label_Y),
        optimal_leaf_order =True
    )
    return component


# @app.callback(
#     Output("output_button_test_script", "children"),
#     [Input("test_script_button", "n_clicks")]
# )
# def testing_script_calling_by_button(n_clicks):
#     if n_clicks >= 1:
#         blop = "script"
#         return os.system("python3 {}_test.py".format(blop))
#     else:
#         return dash.no_update




if __name__ == "__main__":
    app.run_server(debug=True)
