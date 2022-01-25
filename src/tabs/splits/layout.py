import dash_bootstrap_components as dbc
from dash import html

_introductionNotice = html.Div(className="fig_group_all_width", children=[
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
])

__dataFile = dbc.FormGroup(
    [
        dbc.Label("Data file(s) *", className="form_labels"),
        dbc.Input(id="path_to_data_file", placeholder="Enter path",
                  className="form_input_text"),
        dbc.FormText(
            "Write the path to the data files (spectra). You can use either absolute or relative path.",
        ),
    ],
    className="form_field"
)

__metaDataFile = dbc.FormGroup(
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
)

__outputFile = dbc.FormGroup(
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
)

__useRawData = dbc.FormGroup(
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
)

_file = html.Div(className="title_and_form", children=[
    html.H4(id="CreateSplits_paths_title", children="A) Files"),
    dbc.Form(children=[
        dbc.Col(children=[__dataFile, __metaDataFile, __outputFile, __useRawData
                          ]),

    ]),

])

__posNegPairing = dbc.FormGroup(
    [
        dbc.Checklist(
            id="in_pairing_pos_neg",
            options=[
                {"label": "Pos and Neg pairing",
                 "value": 0},
            ],
            labelCheckedStyle={"color": "#13BD00"},
        )
    ],
)

__posPattern = dbc.FormGroup(
    [
        dbc.Input(id="distinct_id_pos_samples",
                  className="form_input_text",
                  placeholder="Pattern for positive samples"),
    ],
)

__negPattern = dbc.FormGroup(
    [
        dbc.Input(id="distinct_id_neg_samples",
                  className="form_input_text",
                  placeholder="Pattern for negative samples"),
    ],
)

__otherPairing = dbc.FormGroup(
    [
        dbc.Checklist(
            id="in_pairing_samples",
            options=[
                {"label": "Other pairing", "value": 0},
            ],
            labelCheckedStyle={"color": "#13BD00"},
        )
    ],
)

_type1Pattern = dbc.FormGroup(
    [
        dbc.Input(id="distinct_id_1_samples",
                  className="form_input_text",
                  placeholder="Pattern for type 1 of samples"),
    ],
)

_type2Pattern = dbc.FormGroup(
    [
        dbc.Input(id="distinct_id_2_samples",
                  className="form_input_text",
                  placeholder="Pattern for type 2 of samples"),
    ],
)

_dataFusion = html.Div(className="title_and_form", children=[
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
            __posNegPairing,
            html.Div(id="div_pair_pn", children=[
                __posPattern,
                __negPattern
            ], style={'display': 'none'}),
            __otherPairing,
            html.Div(id="div_pair_12", children=[
                _type1Pattern,
                _type2Pattern
            ], style={"display": "none"}),

        ])
    ])
])

splitsLayout = dbc.Tab(className="global_tab",
                       label="Splits",
                       children=[_introductionNotice,
                                 html.Div(className="fig_group",
                                          children=[_file,
                                                    _dataFusion,
                                                    ]),

                                 html.Div(className="fig_group", children=[
                                     html.Div(className="title_and_form",
                                              children=[
                                                  html.H4(id="Exp_desg_title",
                                                          children="C) Define Experimental designs"),
                                                  dbc.Form(children=[
                                                      dbc.Col(children=[

                                                          dbc.FormText(
                                                              "Allows to link each file to its type/group to separate them approprietly afterwards."
                                                          ),
                                                          dbc.Card([
                                                              dbc.FormGroup(
                                                                  [
                                                                      dbc.Label(
                                                                          "Name of the targets column"),
                                                                      dbc.RadioItems(
                                                                          id="in_target_col_name",
                                                                          value=0,
                                                                          inline=True),
                                                                  ],
                                                                  className="form_field"
                                                              ),
                                                              dbc.FormGroup(
                                                                  [
                                                                      dbc.Label(
                                                                          "Name of the unique id column"),
                                                                      dbc.RadioItems(
                                                                          id="in_ID_col_name",
                                                                          value=0,
                                                                          inline=True),
                                                                  ],
                                                                  className="form_field"
                                                              )],
                                                              body=True
                                                          ),
                                                          html.Br(),
                                                          dbc.FormText(
                                                              "Define labels and filter out samples."
                                                          ),
                                                          dbc.Card(id="",
                                                                   children=[
                                                                       dbc.FormGroup(
                                                                           [
                                                                               dbc.Label(
                                                                                   "Type of classification"),
                                                                               dbc.RadioItems(
                                                                                   id="in_classification_type",
                                                                                   value=0,
                                                                                   inline=True,
                                                                                   options=[
                                                                                       {
                                                                                           "label": "Binary",
                                                                                           "value": 0},
                                                                                       {
                                                                                           "label": "Multiclass",
                                                                                           "value": 1,
                                                                                           "disabled": True},
                                                                                   ]),
                                                                           ],
                                                                           className="form_field"
                                                                       ),
                                                                       dbc.FormGroup(
                                                                           [
                                                                               dbc.Label(
                                                                                   "Labels"),
                                                                               html.Div(
                                                                                   className="fig_group_mini",
                                                                                   id="define_classes_desgn_exp",
                                                                                   children=[
                                                                                       dbc.Input(
                                                                                           id="class1_name"),
                                                                                       dbc.Checklist(
                                                                                           id="possible_groups_for_class1"),
                                                                                       dbc.Input(
                                                                                           id="class2_name"),
                                                                                       dbc.Checklist(
                                                                                           id="possible_groups_for_class2")
                                                                                   ])
                                                                           ],
                                                                           className="form_field"
                                                                       ),
                                                                       dbc.Button(
                                                                           "Add",
                                                                           id="btn_add_design_exp",
                                                                           color="primary",
                                                                           className="custom_buttons",
                                                                           n_clicks=0),
                                                                       html.Div(
                                                                           id="output_btn_add_desgn_exp")

                                                                   ],
                                                                   body=True),
                                                      ]),

                                                  ]),

                                              ]),
                                     html.Div(className="title_and_form",
                                              children=[
                                                  html.H4(
                                                      id="Define_split_title",
                                                      children="D) Define splits"),
                                                  dbc.Form(children=[
                                                      dbc.Col(children=[
                                                          dbc.FormGroup([
                                                              dbc.Label(
                                                                  "Proportion of samples in test"),
                                                              dbc.Input(
                                                                  id="in_percent_samples_in_test",
                                                                  value="0.2",
                                                                  type="number",
                                                                  min=0, max=1,
                                                                  step=0.01,
                                                                  size="5")
                                                          ],
                                                              className="form_field"),
                                                          dbc.FormGroup([
                                                              dbc.Label(
                                                                  "Number of splits"),
                                                              dbc.Input(
                                                                  id="in_nbr_splits",
                                                                  value="25",
                                                                  type="number",
                                                                  min=1,
                                                                  size="5"),
                                                          ],
                                                              className="form_field"),
                                                          dbc.FormGroup([
                                                              dbc.Label(
                                                                  "Peak Threshold"),
                                                              dbc.Input(
                                                                  id="in_peak_threshold_value",
                                                                  value="500",
                                                                  type="number",
                                                                  min=1,
                                                                  size="5")
                                                          ],
                                                              className="form_field"),
                                                          dbc.FormGroup([
                                                              dbc.Label(
                                                                  "AutoOptimize number"),
                                                              dbc.Input(
                                                                  id="in_autoOptimize_value",
                                                                  value="20",
                                                                  type="number",
                                                                  min=1,
                                                                  size="5")
                                                          ],
                                                              className="form_field"),
                                                      ]),
                                                  ])
                                              ]),

                                 ]),
                                 html.Div(className="fig_group", children=[
                                     html.Div(className="title_and_form",
                                              children=[
                                                  html.H4(id="preprocess_title",
                                                          children="E) Other Preprocessing"),
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
                                                                                  dbc.Label(
                                                                                      "Processing according to data type"),
                                                                                  dbc.FormText(
                                                                                      "LDTD1 means the preprocessing will be done on all samples in one time. "
                                                                                      "LDTD2 means the preprocessing will be done seperatly for each split."),
                                                                                  dbc.RadioItems(
                                                                                      id="in_type_of_data",
                                                                                      value="none",
                                                                                      inline=True,
                                                                                      options=[
                                                                                          {
                                                                                              "label": "None",
                                                                                              "value": "none"},
                                                                                          {
                                                                                              "label": "LDTD 1",
                                                                                              "value": "LDTD1"},
                                                                                          {
                                                                                              "label": "LDTD 2",
                                                                                              "value": "LDTD2"},
                                                                                      ]),
                                                                              ],
                                                                              className="form_field"
                                                                          ),
                                                                          dbc.FormGroup(
                                                                              [
                                                                                  dbc.Label(
                                                                                      "Perform peak picking"),
                                                                                  dbc.RadioItems(
                                                                                      id="in_peak_picking",
                                                                                      value=0,
                                                                                      inline=True,
                                                                                      options=[
                                                                                          {
                                                                                              "label": "No",
                                                                                              "value": 0,
                                                                                              "disabled": True},
                                                                                          {
                                                                                              "label": "Yes",
                                                                                              "value": 1,
                                                                                              "disabled": True},
                                                                                      ]),
                                                                              ],
                                                                              className="form_field"
                                                                          ),
                                                                          dbc.FormGroup(
                                                                              [
                                                                                  dbc.Label(
                                                                                      "Perform alignment"),
                                                                                  dbc.RadioItems(
                                                                                      id="in_alignment",
                                                                                      value=0,
                                                                                      inline=True,
                                                                                      options=[
                                                                                          {
                                                                                              "label": "No",
                                                                                              "value": 0,
                                                                                              "disabled": True},
                                                                                          {
                                                                                              "label": "Yes",
                                                                                              "value": 1,
                                                                                              "disabled": True},
                                                                                      ]),
                                                                              ],
                                                                              className="form_field"
                                                                          ),
                                                                          dbc.FormGroup(
                                                                              [
                                                                                  dbc.Label(
                                                                                      "Perform normalization"),
                                                                                  dbc.RadioItems(
                                                                                      id="in_normalization",
                                                                                      value=0,
                                                                                      inline=True,
                                                                                      options=[
                                                                                          {
                                                                                              "label": "No",
                                                                                              "value": 0,
                                                                                              "disabled": True},
                                                                                          {
                                                                                              "label": "Yes",
                                                                                              "value": 1,
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
                                     html.Div(className="title_and_form",
                                              children=[
                                                  html.H4(
                                                      id="create_split_title",
                                                      children="F) Generate file"),
                                                  dbc.Form(children=[
                                                      dbc.Col(children=[
                                                          html.Div(
                                                              id="output_button_split_file"),
                                                          html.Div(
                                                              className="button_box",
                                                              children=[
                                                                  html.Div(
                                                                      "Before clicking on the Create button, make shure all field with an * are correctly filled."),
                                                                  dbc.Button(
                                                                      "Create",
                                                                      color="primary",
                                                                      id="split_dataset_button",
                                                                      className="custom_buttons",
                                                                      n_clicks=0),
                                                                  html.Div(
                                                                      id="output_button_split",
                                                                      children="",
                                                                      style={
                                                                          'display': 'none'}),

                                                              ]),

                                                      ])
                                                  ])
                                              ])
                                 ]),

                                 ])
