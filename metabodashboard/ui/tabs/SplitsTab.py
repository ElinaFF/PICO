import dash_bootstrap_components as dbc
import pandas
from dash import html, Output, Input, dash, State, dcc, callback_context, ALL
from dash.dcc import send_file

from .MetaTab import MetaTab
from ...domain import MetaboController
from ...service import Utils

EXP_NAME = []


class SplitsTab(MetaTab):

    def __init__(self, app: dash.Dash, metabo_controller: MetaboController):
        super().__init__(app, metabo_controller)

    def getLayout(self) -> dbc.Tab:
        _introductionNotice = html.Div(className="fig_group_all_width", children=[
            dbc.Card(children=[
                dbc.CardBody(
                    [
                        html.Div(
                            "In this tab, you will create a setting file with all info necessary "
                            "to run a machine learning experiment. An * besides the name of the field means a value "
                            "is required, all other fields can be left untouched and will use default values."),
                    ]
                    # This file will even contain a copy of the data "
                    # "to avoid broken paths (after some times, files might be moved or deleted and the path pointing "
                    # "to their location will then be not valid).
                ),
            ]),
        ])

        __dataFile = html.Div(
            [
                dbc.Label("Data file(s) *", className="form_labels"),
                html.Div([
                    dcc.Upload(id="upload_datatable",
                               children=[dbc.Button("Upload File",
                                                    id="upload_datatable_button",
                                                    # className="custom_buttons",
                                                    color="outline-primary")]),
                    dcc.Loading(id="upload_datatable_loading", children=[
                        html.Div(id="upload_datatable_output", style={"color": "green"})
                    ], style={"width": "100%"}, type="dot", color="#13BD00"),
                ], style={"display": "flex", "align-items": "center"}),
                dbc.FormText(
                    "You can give a Progenesis abundance file, or a matrix with samples as lines and features as "
                    "columns.",
                ),
            ],
            className="form_field"
        )

        __metaDataFile = html.Div(
            [
                dbc.Label(className="form_labels", children=[html.Span("Metadata file  "), html.Span(
                    "(optionnal if Progenesis matrix given)", style={"font-size": "0.9em", "text-transform": "none"})]),
                html.Div([
                    dcc.Upload(id="upload_metadata",
                               children=[dbc.Button("Upload File",
                                                    id="upload_metadata_button",
                                                    # className="custom_buttons",
                                                    color="outline-primary")]),
                    dcc.Loading(id="upload_metadata_loading", children=[
                        html.Div(id="upload_metadata_output", style={"color": "green"})
                    ], style={"width": "100%"}, type="dot", color="#13BD00"),
                ], style={"display": "flex", "align-items": "center"}),
                dbc.FormText(
                    "The metadata file should at least contain : one column with samples name corresponding to names in the"
                    "data file, and one column of target/class/condition.",
                )
            ],
            className="form_field"
        )

        __outputFile = html.Div(
            [
                dbc.Label("Output file *",
                          className="form_labels"),
                dbc.Input(id="name_splits_batch",

                          placeholder="Enter Name",
                          className="form_input_text"),
                dbc.FormText(
                    "Give a name to the output file, it will have this format : 'DD-MM-YYYY_CUSTOMNAME.metaboexpe'.",
                ),
            ],
            className="form_field"
        )

        __useRawData = html.Div(
            [
                dbc.Label("Use raw data",
                          className="form_labels"),
                dbc.FormText(
                    "If there is normalized and raw data in your file, you can choose to use raw by selecting yes. "
                    "Default is no and will use normalized data.",
                ),
                dbc.RadioItems(
                    id="in_use_raw",

                    options=[
                        {"label": "Yes", "value": True},
                        {"label": "No", "value": False}
                    ],
                    value=False,
                    labelCheckedStyle={"color": "#13BD00"},
                ),

            ],
            className="form_field"
        )

        _file = html.Div(className="title_and_form", children=[
            html.H4(id="CreateSplits_paths_title", children="A) Files"),
            dbc.Form(children=[
                dbc.Col(children=[__useRawData, __dataFile, __metaDataFile, __outputFile
                                  ]),

            ]),

        ])

        __typeGroupLink = dbc.Card([
            html.Div(
                [
                    dbc.Label(
                        "Name of the targets column"),
                    dbc.RadioItems(
                        id="in_target_col_name",
                        options=Utils.format_list_for_checklist(self.metabo_controller.get_metadata_columns()),
                        value=self.metabo_controller.get_target_column(),
                        inline=True),
                ],
                className="form_field"
            ),
            html.Div(
                [
                    dbc.Label(
                        "Name of the unique id column"),
                    dbc.RadioItems(
                        id="in_ID_col_name",

                        options=Utils.format_list_for_checklist(self.metabo_controller.get_metadata_columns()),
                        value=self.metabo_controller.get_id_column(),
                        inline=True),
                ],
                className="form_field"
            ),
            html.Div(
                id="info_progenesis_loaded",
                style={"color": "grey", "padding-left": "2em", "font-style": "italic"}
            )],
            body=True
        )

        __labelDefinition = dbc.Card(id="",
                                     children=[
                                         html.Div(
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
                                         html.Div(
                                             [
                                                 dbc.Label(
                                                     "Labels"),
                                                 html.Div(
                                                     className="fig_group_mini",
                                                     id="define_classes_desgn_exp",
                                                     children=[
                                                         dbc.Input(
                                                             id="class1_name",
                                                             type="text",
                                                         ),
                                                         dbc.Checklist(
                                                             id="possible_groups_for_class1",
                                                         ),
                                                         dbc.Input(
                                                             id="class2_name",
                                                         ),
                                                         dbc.Checklist(
                                                             id="possible_groups_for_class2",
                                                         )
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
                                     ], body=True)

        _experimentalDesigns = html.Div(className="title_and_form",
                                        children=[
                                            html.H4(id="Exp_desg_title",
                                                    children="B) Define Experimental designs"),
                                            dbc.Form(
                                                children=[
                                                    dbc.Col(children=[

                                                        dbc.FormText(
                                                            "Link each sample to its target/class."
                                                        ),
                                                        __typeGroupLink
                                                        ,
                                                        html.Br(),
                                                        dbc.FormText(
                                                            "Experimental Designs."
                                                        ),
                                                        dbc.Card(id="setted_classes_container",
                                                                 children=self._get_wrapped_experimental_designs(),
                                                                 style={"display": "block", "padding": "1em"}),
                                                        dbc.FormText(
                                                            "Define labels and filter out samples."
                                                        ),
                                                        __labelDefinition
                                                        ,
                                                    ]),

                                                ]),
                                        ])

        _dataFusion = html.Div(className="title_and_form", children=[
            html.H4(id="sep_samples_title", children="C) Data Fusion"),
            dbc.Form(children=[
                dbc.Col([
                    dbc.FormText("Pairing list."),
                    dbc.Card(id="setted_pairings_container", children=self._get_wrapped_pairings(),
                             style={"padding": "1em"}),
                    dbc.FormText("Select the type of data fusion you want to use."),
                    dbc.Card([
                        html.Div([
                            html.Span([
                                dbc.Label("Type"),
                                dbc.Select(options=[
                                    {"label": "None", "value": "none"},
                                    {"label": "Group", "value": "group"},
                                    {"label": "Pattern", "value": "pattern"},
                                ],
                                    id="pairing_type",
                                    value="none",
                                    className="form_select",
                                    style={"width": "90%"}),
                            ], style={"min-width": "25%"}),
                            html.Span([
                                dbc.Label("Column(s)"),
                                html.Div(id="pairing_columns", children=[
                                    dcc.Dropdown(
                                        self.metabo_controller.get_metadata_columns(),
                                        id="pairing_group_column",
                                        style={"display": "none"}
                                    ),
                                    dcc.Dropdown(
                                        self.metabo_controller.get_metadata_columns(),
                                        id={'index': "pairing_pattern_column_1", "type": "pattern"},
                                        style={"display": "none"}
                                    ),
                                    dcc.Dropdown(
                                        self.metabo_controller.get_metadata_columns(),
                                        id={'index': "pairing_pattern_column_2", "type": "pattern"},
                                        style={"display": "none"}
                                    ),
                                    dcc.Dropdown(
                                        self.metabo_controller.get_metadata_columns(),
                                        id={'index': "pairing_pattern_column_3", "type": "pattern"},
                                        style={"display": "none"}
                                    )
                                ]),
                            ], style={"min-width": "75%"})
                        ], style={"display": "flex", "flex-direction": "row"}),
                        html.Div(id="error_pairing_type", style={"color": "red"}),
                        dbc.Button(
                            "Set pairing",
                            id="btn_add_pairing",
                            color="primary",
                            className="custom_buttons",
                            n_clicks=0,
                            style={"width": "22.5%", "margin": "1em 0 0 0"}),
                    ], style={"padding": "1em"}),
                ])
            ])
        ])

        __sampleProportion = html.Div([
            dbc.Label(
                "Proportion of samples in test"),
            dbc.Input(
                id="in_percent_samples_in_test",

                value=self.metabo_controller.get_train_test_proportion(),
                type="number",
                min=0, max=1,
                step=0.01,
                size="5")
        ], className="form_field")

        __splitsNumber = html.Div([
            dbc.Label(
                "Number of splits"),
            dbc.Input(
                id="in_nbr_splits",

                value=self.metabo_controller.get_number_of_splits(),
                type="number",
                min=1,
                size="5"),
        ],
            className="form_field")

        _splitDefinition = html.Div(className="title_and_form",
                                    children=[
                                        html.H4(
                                            id="Define_split_title",
                                            children="D) Define splits"),
                                        dbc.Form(children=[
                                            dbc.Col(children=[__sampleProportion,
                                                              __splitsNumber
                                                              ]),
                                        ])
                                    ])
        __LDTDDataType = html.Div(
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
            ], className="form_field")

        __LDTDPeakPicking = html.Div(
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
            ], className="form_field")

        __LDTDAlignment = html.Div(
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
        )

        __LDTDNormalization = html.Div(
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
            ], className="form_field")

        __peakThreshold = html.Div([
            dbc.Label(
                "Peak Threshold"),
            dbc.Input(
                id="in_peak_threshold_value",

                value="500",
                type="number",
                min=1,
                size="5")
        ], className="form_field")

        __autoOptimizeNumber = html.Div([
            dbc.Label(
                "AutoOptimize number"),
            dbc.Input(
                id="in_autoOptimize_value",

                value="20",
                type="number",
                min=1,
                size="5")
        ], className="form_field")

        _otherProcessing = html.Div(className="title_and_form",
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
                                                            children=[__LDTDDataType,
                                                                      __LDTDPeakPicking,
                                                                      __LDTDAlignment,
                                                                      __LDTDNormalization,
                                                                      __peakThreshold,
                                                                      __autoOptimizeNumber
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
                                    ])

        _generateFile = html.Div(className="title_and_form",
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

        return dbc.Tab(className="global_tab",
                       label="Splits",
                       children=[_introductionNotice,
                                 html.Div(className="fig_group",
                                          children=[_file,
                                                    _experimentalDesigns,
                                                    ]),

                                 html.Div(className="fig_group",
                                          children=[_dataFusion,
                                                    _splitDefinition
                                                    ]),

                                 html.Div(className="fig_group",
                                          children=[_otherProcessing,
                                                    _generateFile
                                                    ]),
                                 dcc.Download(id="download-save-file-split")
                                 ])

    def _registerCallbacks(self) -> None:
        @self.app.callback(
            [Output('info_progenesis_loaded', 'children'),
             Output('upload_datatable_output', 'children'),
             Output('upload_datatable_output', 'style')],
            [Input('upload_datatable', 'contents')],
            [State('upload_datatable', 'filename'),
             State("in_use_raw", "value")
             ]
        )
        def upload_data(list_of_contents, list_of_names, use_raw):
            if list_of_contents is not None:
                try:
                    self.metabo_controller.set_data_matrix_from_path(list_of_names,
                                                                     data=list_of_contents,
                                                                     use_raw=use_raw)
                except TypeError as err:
                    return dash.no_update, [html.P(str(err))], {"color": "red"}
                except pandas.errors.ParserError as err:
                    return dash.no_update, [html.P("Rows must have an equal number of columns")], {"color": "red"}
                self.metabo_controller.reset_experimental_designs()

                if self.metabo_controller.is_progenesis_data():
                    # trigger the update of possible targets
                    return "Info: Selection not needed, handled by Progenesis.", [
                        html.P(f"\"{list_of_names}\" has successfully been uploaded !")], {"color": "green"}
                return "", [html.P(f"\"{list_of_names}\" has successfully been uploaded !")], {"color": "green"}
            else:
                return dash.no_update, dash.no_update, dash.no_update

        @self.app.callback([Output("in_target_col_name", "options"),
                            Output("in_ID_col_name", "options"),
                            Output("upload_metadata_output", "children"),
                            Output("upload_metadata_output", "style")],
                           [Input('upload_metadata', 'contents')],
                           [State('upload_metadata', 'filename')]
                           )
        def get_metadata_cols_names_to_choose_from(list_of_contents, list_of_names):
            if list_of_contents is not None:
                try:
                    self.metabo_controller.set_metadata(list_of_names, data=list_of_contents)
                except TypeError as err:
                    return [], [], html.P(str(err)), {"color": "red"}
                formatted_columns = Utils.format_list_for_checklist(self.metabo_controller.get_metadata_columns())
                self.metabo_controller.reset_experimental_designs()
                return formatted_columns, formatted_columns, html.P(
                    f"\"{list_of_names}\" has successfully been uploaded !"), {"color": "green"}
            else:
                return dash.no_update

        @self.app.callback(
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
                                html.Div(
                                    [
                                        dbc.Label("Label 1"),
                                        dbc.Input(id="class1_name",
                                                  placeholder="Enter name",
                                                  debounce=True,
                                                  className="form_input_text"),

                                    ],
                                    className="form_field"
                                ),
                                html.Div(
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
                                html.Div(
                                    [
                                        dbc.Label("Label 2"),
                                        dbc.Input(id="class2_name",
                                                  placeholder="Enter name",
                                                  debounce=True,
                                                  className="form_input_text"),

                                    ],
                                    className="form_field"
                                ),
                                html.Div(
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

        @self.app.callback(
            [Output("possible_groups_for_class1", "options"),
             Output("possible_groups_for_class2", "options"),
             Output("output_btn_add_desgn_exp", "children"),
             Output("in_target_col_name", "value")],
            [Input("in_target_col_name", "value"),
             Input('info_progenesis_loaded', 'children')],
        )
        def update_possible_classes_exp_design(target_col, children):
            triggered_id = callback_context.triggered[0]["prop_id"].split(".")[0]

            if triggered_id == "in_target_col_name":
                self.metabo_controller.set_target_column(target_col)
                formatted_possible_targets = Utils.format_list_for_checklist(
                    self.metabo_controller.get_unique_targets()
                )
                return formatted_possible_targets, formatted_possible_targets, "", target_col
            elif triggered_id == "info_progenesis_loaded":
                formatted_possible_targets = Utils.format_list_for_checklist(
                    self.metabo_controller.get_unique_targets()
                )
                return formatted_possible_targets, formatted_possible_targets, "", None
            else:
                return [], [], "", self.metabo_controller.get_target_column()

        @self.app.callback(
            [Output("class1_name", "value"),
             Output("possible_groups_for_class1", "value"),
             Output("class2_name", "value"),
             Output("possible_groups_for_class2", "value"),
             Output("setted_classes_container", "children"),
             Output("setted_classes_container", "style")],
            [Input("btn_add_design_exp", "n_clicks"),
             Input("remove_experimental_design_button", "n_clicks"),
             Input("in_target_col_name", "value"),
             Input("info_progenesis_loaded", "children")],
            [State("class1_name", "value"),
             State("possible_groups_for_class1", "value"),
             State("class2_name", "value"),
             State("possible_groups_for_class2", "value")],
        )
        def add_n_reset_classes_exp_design(n_add, n_remove, target_col, children, c1, g1, c2, g2):
            triggered_id = callback_context.triggered[0]["prop_id"].split(".")[0]

            if triggered_id == "remove_experimental_design_button" or triggered_id == "in_target_col_name" or \
                    triggered_id == "info_progenesis_loaded":
                self.metabo_controller.reset_experimental_designs()
            elif triggered_id == "btn_add_design_exp":
                self.metabo_controller.add_experimental_design({c1: g1, c2: g2})

            return "", 0, "", 0, self._get_wrapped_experimental_designs(), {"display": "block", "padding": "1em"}

        @self.app.callback(
            Output("pairing_columns", "children"),
            [Input("pairing_type", "value")]
        )
        def define_pairing_columns(pairing_type):
            if pairing_type == "group":
                return [
                    dcc.Dropdown(
                        self.metabo_controller.get_metadata_columns(),
                        id="pairing_group_column",
                    ),
                    dcc.Dropdown(
                        self.metabo_controller.get_metadata_columns(),
                        id={'index': "pairing_pattern_column_1", "type": "pattern"},
                        style={"display": "none"}
                    ),
                    dcc.Dropdown(
                        self.metabo_controller.get_metadata_columns(),
                        id={'index': "pairing_pattern_column_2", "type": "pattern"},
                        style={"display": "none"}
                    ),
                    dcc.Dropdown(
                        self.metabo_controller.get_metadata_columns(),
                        id={'index': "pairing_pattern_column_3", "type": "pattern"},
                        style={"display": "none"}
                    )
                ]
            elif pairing_type == "pattern":
                return [
                    dcc.Dropdown(
                        self.metabo_controller.get_metadata_columns(),
                        id="pairing_group_column",
                        style={"display": "none"}
                    ),
                    dcc.Dropdown(
                        self.metabo_controller.get_metadata_columns(),
                        id={'index': "pairing_pattern_column_1", "type": "pattern"}
                    ),
                    dcc.Dropdown(
                        self.metabo_controller.get_metadata_columns(),
                        id={'index': "pairing_pattern_column_2", "type": "pattern"}
                    ),
                    dcc.Dropdown(
                        self.metabo_controller.get_metadata_columns(),
                        id={'index': "pairing_pattern_column_3", "type": "pattern"}
                    )
                ]
            return [
                dcc.Dropdown(
                    self.metabo_controller.get_metadata_columns(),
                    id="pairing_group_column",
                    style={"display": "none"}
                ),
                dcc.Dropdown(
                    self.metabo_controller.get_metadata_columns(),
                    id={'index': "pairing_pattern_column_1", "type": "pattern"},
                    style={"display": "none"}
                ),
                dcc.Dropdown(
                    self.metabo_controller.get_metadata_columns(),
                    id={'index': "pairing_pattern_column_2", "type": "pattern"},
                    style={"display": "none"}
                ),
                dcc.Dropdown(
                    self.metabo_controller.get_metadata_columns(),
                    id={'index': "pairing_pattern_column_3", "type": "pattern"},
                    style={"display": "none"}
                )
            ]

        @self.app.callback(
            Output("pairing_type", "value"),
            [Input("upload_metadata", "filename")]
        )
        def update_pairing_type(filename):
            return "none"

        @self.app.callback(
            [Output("setted_pairings_container", "children"),
             Output("error_pairing_type", "children")],
            [Input("btn_add_pairing", "n_clicks"),
             Input("remove_pairing_button", "n_clicks")],
            [State("pairing_type", "value"),
             State("pairing_group_column", "value"),
             State({'index': ALL, "type": "pattern"}, "value")
             ]
        )
        def add_n_reset_pairings(n_add, n_remove, pairing_type, pairing_group_column, pairing_pattern_columns):
            triggered_id = callback_context.triggered[0]["prop_id"].split(".")[0]
            actual_pairing_columns = self.metabo_controller.get_pairing_columns()

            if triggered_id == "remove_pairing_button":
                self.metabo_controller.reset_pairing_columns()
            elif triggered_id == "btn_add_pairing":
                pairing_pattern_columns = [column for column in pairing_pattern_columns if column is not None]

                if pairing_type == "group":
                    pairing = pairing_group_column
                elif pairing_type == "pattern":
                    pairing = pairing_pattern_columns
                else:
                    pairing = None

                try:
                    self.metabo_controller.add_pairing_columns(pairing, pairing_type)
                except ValueError as e:
                    return dash.no_update, str(e)

            return self._get_wrapped_pairings(), ""

        @self.app.callback(
            Output("collapse_preprocessing", "is_open"),
            [Input("collapse_preprocessing_button", "n_clicks")],
            [State("collapse_preprocessing", "is_open")],
        )
        def toggle_collapse_preprocessing(n, is_open):
            if n:
                return not is_open
            return is_open

        @self.app.callback(
            Output("in_ID_col_name", "value"),
            [Input("in_ID_col_name", "value")]
        )
        def update_ID_col_name(new_value):
            if new_value is not None:
                self.metabo_controller.set_id_column(new_value)
            return self.metabo_controller.get_id_column()

        @self.app.callback(
            Output("in_nbr_splits", "value"),
            [Input("in_nbr_splits", "value")]
        )
        def update_nbr_splits(new_value):
            if callback_context.triggered[0]["prop_id"] == ".":
                return self.metabo_controller.get_number_of_splits()
            try:
                casted_value = int(new_value)
            except (ValueError, TypeError):
                return new_value
            self.metabo_controller.set_number_of_splits(int(casted_value))
            return casted_value

        @self.app.callback(
            Output("in_percent_samples_in_test", "value"),
            [Input("in_percent_samples_in_test", "value")]
        )
        def update_percent_samples_in_test(new_value):
            if callback_context.triggered[0]["prop_id"] == ".":
                return self.metabo_controller.get_train_test_proportion()
            try:
                casted_value = float(new_value)
            except (ValueError, TypeError):
                return new_value
            self.metabo_controller.set_train_test_proportion(casted_value)
            return casted_value

        @self.app.callback(
            [Output('output_button_split_file', 'children'),
             Output("download-save-file-split", "data")],
            [Input('split_dataset_button', 'n_clicks')],
            [State("name_splits_batch", "value"),
             State("in_use_raw", "value"),
             State('in_nbr_splits', 'value'),
             State('in_nbr_processes', 'value'),
             # State("path_to_data_file", "value"),
             State('in_peak_threshold_value', 'value'),
             State('in_percent_samples_in_test', 'value'),
             State('in_autoOptimize_value', 'value'),
             # State('in_path_to_metadata', 'value'),
             State('in_ID_col_name', 'value'),
             State('in_target_col_name', 'value'),
             State("in_type_of_data", "value"),
             State("in_peak_picking", "value"),
             State("in_alignment", "value"),
             State("in_normalization", "value")
             ]
        )
        def saving_params_of_splits_batch(n, name_of_the_file, use_raw, nbr_splits, nbr_processes,  # path_data_files,
                                          peakT, percent_in_test, autoOpt, ID_col_name,  # path_to_metadata,
                                          targets_col_name,
                                          type_of_processing, peak_pick, align, normalize):
            """
            Create the file (json) which will contains all info about the split creation / data experiment.
            """
            if n >= 1:
                self.metabo_controller.create_splits()
                Utils.dump_metabo_expe(self.metabo_controller.generate_save())

                return "The parameters file is created, the splits's creation should start shortly...", \
                       send_file(Utils.get_metabo_experiment_path())
            else:
                return dash.no_update, dash.no_update

    def _get_wrapped_experimental_designs(self):
        children_container = [html.Div("Experimental design")]
        all_experimental_designs = self.metabo_controller.get_all_experimental_designs_names()

        if len(all_experimental_designs) == 0:
            button = html.Div(
                dbc.Button("Reset", className="custom_buttons", id="remove_experimental_design_button"),
                style={"display": "none"}
            )
            return html.Div([html.P("No experimental design setted yet."), button])

        for _, full_name in all_experimental_designs:
            children_container.append(html.Div(children=["- " + full_name],
                                               style={"display": "flex",
                                                      "justify-content": "space-between", "align-items": "center"})
                                      )
        button = html.Div(
            dbc.Button("Reset", className="custom_buttons", id="remove_experimental_design_button"),
            style={"textAlign": "right"}
        )
        children_container.append(button)
        return children_container

    def _get_wrapped_pairings(self):
        pairing_columns = self.metabo_controller.get_pairing_columns()

        if not pairing_columns.get("group") and not pairing_columns.get("pattern"):
            button = html.Div(
                dbc.Button("Reset", className="custom_buttons", id="remove_pairing_button"),
                style={"display": "none"}
            )
            return [html.Div([html.P("No pairing setted yet."), button])]
        children_container = []
        group_pairing_columns = pairing_columns.get("group")
        pattern_pairing_columns = pairing_columns.get("pattern")
        if group_pairing_columns and group_pairing_columns is not None:
            children_container.append(html.Div(children=["Group pairing columns:"]))
            for column in group_pairing_columns:
                children_container.append(html.Div(children=["- " + column]))
        if pattern_pairing_columns and pattern_pairing_columns is not None:
            children_container.append(html.Div(children=["Pattern pairing columns:"]))
            for column in pattern_pairing_columns:
                children_container.append(html.Div(children=["- " + ", ".join(column)]))
        button = html.Div(
            dbc.Button("Reset", className="custom_buttons", id="remove_pairing_button")
        )
        children_container.append(button)
        return children_container
