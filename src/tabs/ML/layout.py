import dash_bootstrap_components as dbc
from dash import html

__splitConfigFile = dbc.FormGroup(
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

__CVConfig = dbc.FormGroup([
    dbc.Label("Number of Cross Validation folds", className="form_labels"),
    dbc.Input(id="in_nbr_CV_folds", value="5", type="number", min=1,
              size="5")
], className="form_field")

__processNumberConfig = dbc.FormGroup([
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

__availableAlgorithms = dbc.FormGroup(
    [
        dbc.Label("Available Algorithms", className="form_labels"),
        dbc.Checklist(id="in_algo_ML",
                      # inline=True
                      ),
    ],
    className="form_field"
)

__addCustomAlgorithm = dbc.FormGroup(
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

MLLayout = dbc.Tab(className="global_tab", label="Machine Learning",
                   children=[
                       html.Div(className="fig_group", children=[_definitionLearningConfig, _definitionLearningAlgorithm
                                                                 ]),
                   ])
