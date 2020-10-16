import pandas as pd
import numpy as np
import seaborn as sns
import io, base64, glob, datetime, json, importlib
from collections import Counter

import dash, dash_bio
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_bootstrap_components as dbc

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
import umap

import plotly.graph_objs as go

from LearnConfig import *
from ExperimentDesign import *
from Utils import *
from MetaboDashboardConfig import *

from LDTD_CardiaquesMTL_make_split import *
from MetaboDashboard.SamplesPairing import SamplesPairing



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
                                label="Info", children=[
                                html.Div(className="fig_group", children=[
                                    html.Div(className="column_content", children=[
                                        dbc.Card(className="cards_info", children=[
                                            dbc.CardHeader("TODO"),
                                            dbc.CardBody(
                                                [
                                                 html.P("Implement a Toast when split creation is done", className="card-text"),
                                                 html.P("Implement the progression bar for split creation", className="card-text"),
                                                ]
                                            ),
                                        ]),
                                        dbc.Card(className="cards_info", children=[
                                            dbc.CardHeader("Convert"),
                                            dbc.CardBody(
                                                [
                                                    html.P("Blablabla",
                                                           className="card-text"),
                                                ]
                                            ),
                                        ]),
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
                                        dbc.Card("Amazing figure here", className="card_body_fig", body=True),
                                    ])
                                ]),



                         ]),
                        ############
                        # Data tab #
                        ############
                        dbc.Tab(className="global_tab",
                                # tab_style={"margin-left": "auto"},
                                label="Data", children=[
                                html.P("Will allow people to convert their files to the right format... maybe"),
                                html.Div(className="fig_group", children=[

                                ]),
                            ]),
                        #####################
                        # Create splits Tab #
                        #####################
                        dbc.Tab(className="global_tab",
                             label="Create Splits", children=[
                                html.Div("* means the field is mandatory to fill, all other fields can be left untouched and will use default values."),
                                html.Div(className="fig_group", children=[
                                    # html.Div(className="title_and_form", children=[
                                    #     html.H4(id="files_list_title", children="Define the files list"),
                                    #     dbc.Form(children=[
                                    #         dbc.FormText(
                                    #             "This is the file that contains a list of all the data files and a unique number given to each of them."
                                    #             " It allows a simpler and faster way of doing/saving splits. It is preferable to keep this same file for"
                                    #             " all the splits batch with the same dataset.",
                                    #         ),
                                    #         html.Br(),
                                    #         dbc.FormGroup(
                                    #             [
                                    #                 dbc.Label("Does this file already exists *", className="form_labels"),
                                    #                 dbc.RadioItems(
                                    #                     id="list_data_files_exists_or_not",
                                    #                     options=[
                                    #                         {"label": "Yes", "value": 0},
                                    #                         {"label": "No", "value": 1},
                                    #                     ],
                                    #                     inline=True,
                                    #                 ),
                                    #
                                    #             ],
                                    #             className="form_field"
                                    #         ),
                                    #         dbc.Col(id="col_list_data_files", children=[
                                    #             dbc.Input(id="name_files_list"),
                                    #             dbc.Input(id="path_to_data_file"),
                                    #             dbc.Button(id="list_files_button", n_clicks=0)
                                    #         ]),
                                    #         dbc.Toast(
                                    #             "This toast is placed in the top right",
                                    #             id="toast_success_files_list_created",
                                    #             header="Positioned toast",
                                    #             is_open=False,
                                    #             dismissable=True,
                                    #             # icon="success",
                                    #             # top: 66 positions the toast below the navbar
                                    #             # style={"position": "fixed", "top": 66, "right": 10, "width": 350},
                                    #         ),
                                    #         html.Div(id="output_button_list_files", children=[]),
                                    #
                                    #     ])
                                    # ]),
                                    html.Div(className="title_and_form", children=[
                                        html.H4(id="preprocess_title", children="Define Preprocessing"),
                                        dbc.Form(children=[
                                            dbc.Col(children=[
                                                dbc.FormGroup(
                                                    [
                                                        dbc.Label("Processing according to data type"),
                                                        dbc.RadioItems(id="in_type_of_data", value="LCMS",
                                                                       inline=True,
                                                                       options=[
                                                                           {"label": "LC-MS", "value": "LCMS"},
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
                                                                           {"label": "No", "value": 0, "disabled": True},
                                                                           {"label": "Yes", "value": 1, "disabled": True},
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
                                                                           {"label": "No", "value": 0,"disabled": True},
                                                                           {"label": "Yes", "value": 1,"disabled": True},
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
                                                                           {"label": "No", "value": 0,"disabled": True},
                                                                           {"label": "Yes", "value": 1,"disabled": True},
                                                                       ]),
                                                    ],
                                                    className="form_field"
                                                ),
                                            ])
                                        ])
                                    ]),
                                    html.Div(className="title_and_form", children=[
                                        html.H4(id="sep_samples_title", children="Define Sample Pairing"),
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
                                        html.H4(id="CreateSplits_paths_title", children="Define Paths"),
                                        dbc.Form(children=[
                                            dbc.Col(children=[
                                                dbc.FormGroup(
                                                    [
                                                        dbc.Label("Path to data files *", className="form_labels"),
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
                                                        dbc.Label("Unique name for splits batch *", className="form_labels"),
                                                        dbc.Input(id="name_splits_batch", placeholder="Enter Name",
                                                                  className="form_input_text"),
                                                        dbc.FormText(
                                                            "Write a name for this batch of splits that will be used to identify its parameters file",
                                                        ),
                                                    ],
                                                    className="form_field"
                                                ),
                                                # dbc.FormGroup(
                                                #     [
                                                #         dbc.Label("Path to data files", className="form_labels"),
                                                #         dbc.Input(id="in_path_to_data_file", placeholder="Enter path",
                                                #                   className="form_input_text"),
                                                #         dbc.FormText(
                                                #             "Write the path to the data files (spectra). You can use either absolute or relative path.",
                                                #         ),
                                                #     ],
                                                #     className="form_field"
                                                # ),
                                                dbc.FormGroup(
                                                    [
                                                        dbc.Label("Output path for splits", className="form_labels"),
                                                        dbc.Input(id="path_output_splits", placeholder="Enter path",
                                                                  className="form_input_text"),
                                                        dbc.FormText(
                                                            "Write a path where temporary files needed for splits creation will be stored. You can use either absolute or relative path.",
                                                        ),
                                                    ],
                                                    className="form_field"
                                                ),
                                                dbc.FormGroup(
                                                    [
                                                        dbc.Label("Path to metadata file *", className="form_labels"),
                                                        dbc.Input(id="in_path_to_metadata", placeholder="Enter path",
                                                                  debounce=True, className="form_input_text"),
                                                        dbc.FormText(
                                                            "Write the path of the metadata file.You can use either absolute or relative path. "
                                                            "Press Enter when you are done to update other forms.",
                                                        ),
                                                        html.Br(),
                                                        html.Div(id="output_in_case_of_error_in_path_to_metadata")
                                                    ],
                                                    className="form_field"
                                                ),


                                            ]),

                                        ]),

                                    ]),
                                    html.Div(className="title_and_form", children=[
                                        html.H4(id="Exp_desg_title", children="Define Experimental design"),
                                        dbc.Form(children=[
                                            dbc.Col(children=[
                                                dbc.FormGroup([
                                                    dbc.Label("Proportion of samples in test"),
                                                    dbc.Input(id="in_percent_samples_in_test", value="0.2",
                                                              type="number",
                                                              min=0, max=1, step=0.01,
                                                              size="5")
                                                ], className="form_field"),
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
                                                    "Define all group comparaison to test with the algorithms"
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
                                                            dbc.Label("Classes"),
                                                            html.Div(className="fig_group_mini", id="define_classes_desgn_exp", children=[
                                                                dbc.Input(id="class1_name"),
                                                                dbc.Checklist(id="possible_groups_for_class1"),
                                                                dbc.Input(id="class2_name"),
                                                                dbc.Checklist(id="possible_groups_for_class2")
                                                            ])
                                                        ],
                                                        className="form_field"
                                                    ),
                                                    dbc.Button("Add", id="btn_add_design_exp", color="primary", className="custom_buttons", n_clicks=0),
                                                    html.Div(id="output_btn_add_desgn_exp")

                                                ], body=True),
                                            ]),

                                        ]),

                                    ]),

                                ]),
                                html.Div(className="fig_group", children=[
                                    html.Div(className="title_and_form", children=[
                                        html.H4(id="Define_split_title", children="Define splits"),
                                        dbc.Form(children=[
                                            dbc.Col(children=[
                                                dbc.FormGroup([
                                                    dbc.Label("Number of splits"),
                                                    dbc.Input(id="in_nbr_splits", value="25", type="number", min=1,
                                                              size="5"),
                                                ], className="form_field"),
                                                dbc.FormGroup([
                                                    dbc.Label("Number of processes"),
                                                    dbc.Input(id="in_nbr_processes", value="2", type="number", min=1,
                                                              size="5")
                                                ], className="form_field"),
                                                dbc.FormGroup([
                                                    dbc.Label("Peak Threshold"),
                                                    dbc.Input(id="in_peak_threshold_value", value="500", type="number",
                                                              min=1,
                                                              size="5")
                                                ], className="form_field"),
                                                # dbc.FormGroup([
                                                #     dbc.Label("Proportion in test"),
                                                #     dbc.Input(id="in_percent_samples_in_test", value="0.2",
                                                #               type="number",
                                                #               min=0, max=1, step=0.01,
                                                #               size="5")
                                                # ], className="form_field"),
                                                dbc.FormGroup([
                                                    dbc.Label("AutoOptimize number"),
                                                    dbc.Input(id="in_autoOptimize_value", value="20", type="number",
                                                              min=1,
                                                              size="5")
                                                ], className="form_field"),
                                            ]),
                                        ])
                                    ]),
                                    html.Div(className="title_and_form", children=[
                                        html.H4(id="create_split_title", children="Create splits"),
                                        dbc.Form(children=[
                                            dbc.Col(children=[
                                                html.Div(id="output_button_split_file"),
                                                html.Div(className="progress_bar_section", children=[
                                                    dbc.Progress(id="progress", value=0, color="success"),
                                                    html.Div(id="interval_div", children=[])
                                                    # dcc.Interval(id="interval", interval=60000, n_intervals=0),
                                                    # interval is in milliseconds (60 000 => 1min)

                                                    # html.Div(id="output_recursive_split", children="", style={'display': 'none'}),
                                                    # html.Div(id="in_out_nbr_split_created", children="", style={'display': 'none'}),
                                                    # html.Div(id="timer_split", children="", style={'display': 'none'})

                                                ]),
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
                                                            dbc.Checklist(id="in_algo_ML", value="None",
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
                                label="Results",
                                children=[
                                    html.Div(className="Results_info", children=[
                                        dbc.Card(className="results_menu_dropdowns", children=[
                                            dbc.CardBody([
                                                html.Div(className="dropdowns", children=[
                                                    html.H6("Experimental Design : "),
                                                    dbc.Select(id="design_dropdown",
                                                               className="form_select",
                                                               options=[{"label": i, "value": i} for i in
                                                                        EXPERIMENT_DESIGNS],
                                                               value=list(EXPERIMENT_DESIGNS.keys())[0],
                                                               )]
                                                         ),
                                                html.Div(className="dropdowns", children=[
                                                    html.H6("ML Algorithm : "),
                                                    dbc.Select(id="ml_dropdown",
                                                               className="form_select",
                                                               options=[{"label": i, "value": i} for i in
                                                                        LEARN_CONFIG["Algos"]],
                                                               value=list(LEARN_CONFIG["Algos"].keys())[0],
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
                                                html.H6("Current experiment info"),  # , style={"marginTop": 25}
                                                html.Div(id="view_info", children="")
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
                                                            dcc.Loading(
                                                                dcc.Graph(id="accuracy_overview"),
                                                                type="circle")]
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


@app.callback(
    [Output("in_peak_picking", "options")],
    [Input("in_type_of_data", "value")]
)
def enable_disable_preprocessing_options(data_type):
    if data_type != "LCMS":
        return False
    else:
        return dash.no_update

@app.callback(
    [Output("div_pair_pn", "style"),
     Output("div_pair_12", "style")],
    [Input("in_pairing_pos_neg", "value"),
     Input("in_pairing_samples", "value")]
)
def show_hide_name_field_pairing(pair_pn, pair_12):
    if pair_pn == [0] and pair_12 == [0]:
        return {"display": "block"}, {"display": "block"}
    elif pair_pn == [0] and pair_12 != [0]:
        return {"display": "block"}, {"display": "none"}
    elif pair_pn != [0] and pair_12 == [0]:
        return {"display": "none"}, {"display": "block"}
    else:
        return {"display": "none"}, {"display": "none"}



# @app.callback(
#     Output("col_list_data_files", "children"),
#     [Input("list_data_files_exists_or_not", "value")],
# )
# def update_form_define_the_files_list(exists):
#     """
#     If the files already exists (0) the dashboard will only display a form field to ask for the name of the existing file,
#     if it doesn't (1), it will display an extra field to name the output file and a button to launch the creation of the file.
#     :param exists: the value of the radio button -> yes (0) no (1)
#     :return: extra form field and button to adapt to the chosen situation
#     """
#     if exists == 0:
#         return [
#                     dbc.FormGroup(
#                         [
#                             dbc.Label("Name of the file *", className="form_labels"),
#                             dbc.Input(id="name_files_list", placeholder="Enter path",
#                                       className="form_input_text"),
#                             dbc.FormText(
#                                 "Write the name of the file that will be used to store the list of data files."
#                                 "Must end with the '.json' extension.",
#                             ),
#                         ],
#                         className="form_field"
#                     ),
#                 ]
#     elif exists == 1:
#         return [
#                     dbc.FormGroup(
#                         [
#                             dbc.Label("Name of the file *", className="form_labels"),
#                             dbc.Input(id="name_files_list", placeholder="Enter path",
#                                       className="form_input_text"),
#                             dbc.FormText(
#                                 "Write the name of the file that will be used to store the list of data files."
#                                 "Must end with the '.json' extension.",
#                             ),
#                         ],
#                         className="form_field"
#                     ),
#                     dbc.FormGroup(
#                         [
#                             dbc.Label("Path to data files *", className="form_labels"),
#                             dbc.Input(id="path_to_data_file", placeholder="Enter path",
#                                       className="form_input_text"),
#                             dbc.FormText(
#                                 "Write the path to the data files (spectra). You can use either absolute or relative path.",
#                             ),
#                         ],
#                         className="form_field"
#                     ),
#
#                     dbc.Button("Create", color="primary", id="list_files_button",
#                            className="custom_buttons", n_clicks=0)
#                 ]
#


# @app.callback(
#     Output("toast_success_files_list_created", "is_open"),
#     [Input("list_files_button", "n_clicks")],
#     [State("path_to_data_file", "value"),
#      State("name_files_list", "value")]
# )
# def create_list_data_files(n, path_files, name):
#     """
#     Creates a json file containing a dict, the key being a number, and the value being the path to a file (data)
#     :param n: button attribute, indicates number of clicks
#     :param path_files: path of the directory containing the data files
#     :param name: name of the output file containing the list
#     :return: make a success popup visible
#     """
#     if n >= 1:
#         files_list = glob.glob(path_files+"/*")
#         dict = {i : j for i, j in enumerate(files_list)}
#         with open(name, "a+") as infile:
#             json.dump(dict, infile)
#         return True
#     else:
#         return dash.no_update


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
        return [], [], "There is a problem, the format of your metadata file might not be supported. You need to give either a .csv, .xlsY or .odY (where Y replace variation of format). Ex: file.xlsx, file.odt"

    options_list.extend(list(df_metadata.columns))
    print(options_list)
    return [{'label': col, 'value': col} for col in options_list], [{'label': col, 'value': col} for col in options_list], ""


@app.callback(
    Output("define_classes_desgn_exp", "children"),
    [Input("in_classification_type", "value")]
)
def define_classes_for_experiment_design(t):
    if t == 0:
        return [
                html.Div(className="title_and_form_mini", children=[
                    dbc.Form(children=[
                        dbc.Col(children=[
                            dbc.FormGroup(
                                [
                                    dbc.Label("Name of class 1"),
                                    dbc.Input(id="class1_name",
                                              placeholder="Enter name",
                                              debounce=True,
                                              className="form_input_text"),

                                ],
                                className="form_field"
                            ),
                            dbc.FormGroup(
                                [
                                    dbc.Label("Group(s)"),
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
                                    dbc.Label("Name of class 2"),
                                    dbc.Input(id="class2_name",
                                              placeholder="Enter name",
                                              debounce=True,
                                              className="form_input_text"),

                                ],
                                className="form_field"
                            ),
                            dbc.FormGroup(
                                [
                                    dbc.Label("Group(s)"),
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
    Output('output_button_split_file', 'children'),
    [Input('split_dataset_button', 'n_clicks')],
    [State("name_splits_batch", "value"),
     State('in_nbr_splits', 'value'),
     State('in_nbr_processes', 'value'),
     State("path_to_data_file", "value"),
     State('path_output_splits', 'value'),
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
def start_saving_params_of_splits_batch(n, name_of_the_file, nbr_splits, nbr_processes, path_data_files ,path_out_splits,
                                        peakT, percent_in_test, autoOpt, path_to_metadata, ID_col_name, targets_col_name,
                                        type_of_processing, peak_pick, align, normalize, pair_pn, pair_id_pos,
                                        pair_id_neg, pair_12, pair_id_1, pair_id_2):
    """
    Create the skeleton of the file (json) which will contains all info about the split creation launched.
    It will be completed a bit here with inputed infos, and then with each split created, the info about which data file
    is where for each split will be added.
    """
    if n >= 1:
        date_time = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

        # Load the asked experiment design
        with open("temp_exp_designs.json", "r+") as design_file:
            dict_exp_desgn = json.load(design_file)

        # Define a temporary path to output splits files in case needed
        if path_out_splits == "" or path_out_splits is None:
            path_out_splits = "Temp_dir_splits/"

        # Load metadata file as dataframe
        if path_to_metadata.split(".")[-1] == "csv":
            df_metadata = pd.read_csv(path_to_metadata)
        elif "xls" in path_to_metadata.split(".")[-1] or "od" in path_to_metadata.split(".")[-1]:
            df_metadata = pd.read_excel(path_to_metadata)
        else:
            print("There is a problem, the format of your metadata file might not be supported. You need to give either a .csv, .xlsY or .odY (where Y replace variation of format). Ex: file.xlsx, file.odt")

        # Handle paired samples if need be
        if pair_pn == [0]:
            pairing_pn = [pair_id_pos, pair_id_neg]
        else:
            pairing_pn = "no"

        if pair_12 == [0]:
            pairing_12 = [pair_id_1, pair_id_2]
        else:
            pairing_12 = "no"

        # Prepare data for splits creation and handle pairing
        files_list = glob.glob(path_data_files + "/*")
        uniq_ID = list(df_metadata[ID_col_name])
        targets = list(df_metadata[targets_col_name])

        # Do the pairing, all handled by a class : SamplesPairing
        pairing = SamplesPairing([pairing_pn, pairing_12], files_list, targets, uniq_ID, percent_in_test, nbr_splits)
        pairing.split()
        splits_dict = pairing.dict_splits

        # Organizing data to write to config file
        df_metadata = df_metadata.to_dict("list")
        opt_process = [peak_pick, align, normalize]

        split_batch_info = {
            "Date_of_creation": date_time,
            "Directory_temp_splits_file": path_out_splits,
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
            "Splits": splits_dict,
            "Metadata": df_metadata,
        }

        # Writing to config file
        with open(name_of_the_file, "w+") as history_file:
            json.dump(split_batch_info, history_file)
        return "The parameters file is created, the splits's creation should start shortly..."
    else:
        return dash.no_update


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
     State("name_splits_config", "value")]
)
def start_machine_learning(n, selected_algos, split_config_file):
    if n >= 1:
        with open("algo_sklearn.json", "r") as algo_file:
            algo_list = json.load(algo_file)

        algo = []
        for a in selected_algos:
            try:
                # Take the name of an algorithm as a string and add it to the dictionary of global variables
                # The string 'a' now become the variable 'a' to which we assign the imported module of the same name
                # for example, if a="DecisionTreeClassifier", at the end we could do DecisionTreeClassifier.fit()
                new_import = algo_list[a]["importing"]
                globals()[a] = importlib.import_module("." + a, package="sklearn." + new_import)
            except KeyError:
                pass
            except ImportError as ImpErr:
                return "Importing Error: {}. Check if you wrote the right algorithm name or the right package name".format(ImpErr)
            finally:
                algo.append(a)

        with open(split_config_file, "r") as conf_file:
            splits_config = json.load(conf_file)

        # get all files : X_train files [0] and X_test files [1]
        all_data_files = splits_config["Splits"]["split0"][0] + splits_config["Splits"]["split0"][1]

        # Check the processing needed and do it
        if splits_config["Type_of_processing"] != "no":
            opt = splits_config["Options_of_processing"]
            if splits_config["Type_of_processing"] == "LDTD2":
                print("blop")
                # we must do the opposite : assign files to split and then do the processing

            for o in opt:
                print("do option o on all files")

        # Then assign files to splits (create the actuals splits)


        # Compute each algo for each split

        return "Done!"

    else:
        return dash.no_update


@app.callback(
    Output("pop_help_accPlot", "is_open"),
    [Input("help_accPlot", "n_clicks")],
    [State("pop_help_accPlot", "is_open")],
)
def toggle_popover(n, is_open):
    if n:
        return not is_open
    return is_open




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

@app.callback(
    [Output("accuracy_overview", "figure"),
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
        data_matrix_filename = os.path.join("Splits", design_dropdown + "_0")
        with open(data_matrix_filename, "rb") as fi:
            train_df = pkl.load(fi, encoding='bytes')
            train_targets = pkl.load(fi, encoding='latin1')
            test_df = pkl.load(fi, encoding='latin1')
            test_targets = pkl.load(fi, encoding='latin1')

        cols = ["a"] * len(train_df[0])
        train_df = pd.DataFrame(train_df, columns=cols)

        reducer = umap.UMAP()

        def filter_cluster(df, threshold=0.5):
            """
            threshold : (proportion) minimum of non-zero values in a line to consider keeping this line
            for example -> threshold = 0.6 means it will keep only the lines where there is at least 60% of non-zero values
            """
            df = df.T
            nbr_col = len(df.columns.to_list())
            print(nbr_col)
            print((df.astype(bool).sum(axis=0)).shape)
            df_filtered = df.loc[df.astype(bool).sum(axis=1) >= nbr_col*threshold]
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



        for model_filename in glob.glob(os.path.join("Results", design_dropdown+"_*_"+ml_dropdown+"*")):
            with open(model_filename, "rb") as fi:
                gc = pkl.load(fi)
                print(gc.best_estimator_.classes_)
                train_predict = pkl.load(fi)
                test_predict = pkl.load(fi)

            data_matrix_filename = os.path.join("Splits", design_dropdown + "_" + model_filename.split("_")[1])
            with open(data_matrix_filename, "rb") as fi:
                train_df = pkl.load(fi)
                train_targets = pkl.load(fi)
                test_df = pkl.load(fi)
                test_targets = pkl.load(fi)

            splits_name.append(model_filename.split("_")[1])
            split_train_accuracy.append(accuracy_score(y_true=train_targets, y_pred = train_predict))
            split_test_accuracy.append(accuracy_score(y_true=test_targets, y_pred=test_predict))

            if isinstance(gc.best_estimator_, RandomForestClassifier) or \
                isinstance(gc.best_estimator_, DecisionTreeClassifier):
                features_importance = gc.best_estimator_.feature_importances_

            zipped = zip(features_importance, train_df.columns)
            zipped = sorted(zipped, key = lambda t:t[0])

            [features.append(i[1]) for i in zipped if np.abs(i[0]) > 0.0]

        features_count = Counter(features)

        #table = []
        #table_style = {"padding": "12px 55px", "text-align": "left"}
        #table.append(html.Tr([html.Th("Feature", style=table_style), html.Th("Number of models")]))
        #for f in features_count.most_common():
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
                            "Feature":[],
                            "Number of models":[]
                        })

        return fig_acc, df, fig_umap, ""  #.to_dict("records")

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
    metrics_results_train =  {i:[] for i in STATISTICS}
    metrics_results_test =  {i:[] for i in STATISTICS}

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
    Output("view_info", "children")
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
