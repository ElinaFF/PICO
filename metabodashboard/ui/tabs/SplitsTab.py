import dash_bootstrap_components as dbc
from dash import html, Output, Input, dash, State, dcc

from .MetaTab import MetaTab
from ...service import Utils


class SplitsTab(MetaTab):
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
                    #This file will even contain a copy of the data "
                    #"to avoid broken paths (after some times, files might be moved or deleted and the path pointing "
                    #"to their location will then be not valid).
                ),
            ]),
        ])

        __dataFile = html.Div(
            [
                dbc.Label("Data file(s) *", className="form_labels"),
                # dbc.Input(id="path_to_data_file", placeholder="Enter path",
                #           className="form_input_text"),
                dcc.Upload(id="upload_datatable",
                           children=[dbc.Button("Upload File",
                                                id="upload_datatable_button",
                                                # className="custom_buttons",
                                                color="outline-primary")]),
                dbc.FormText(
                    "Write the path to the data files (spectra). You can use either absolute or relative path.",
                ),
            ],
            className="form_field"
        )

        __metaDataFile = html.Div(
            [
                dbc.Label("Metadata file *", className="form_labels"),
                # dbc.Input(id="in_path_to_metadata", placeholder="Enter path",
                #           debounce=True, className="form_input_text"),
                dcc.Upload(id="upload_metadata",
                           children=[dbc.Button("Upload File",
                                                id="upload_metadata_button",
                                                # className="custom_buttons",
                                                color="outline-primary")]),
                dbc.FormText(
                    "Write the path of the metadata file.You can use either absolute or relative path. "
                    "Press Enter when you are done to update other forms.",
                ),
                html.Div(id="output_in_case_of_error_in_path_to_metadata")
            ],
            className="form_field"
        )

        __outputFile = html.Div(
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

        __useRawData = html.Div(
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
                        value=0,
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
                        value=0,
                        inline=True),
                ],
                className="form_field"
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
                                     ], body=True)

        _experimentalDesigns = html.Div(className="title_and_form",
                                        children=[
                                            html.H4(id="Exp_desg_title",
                                                    children="B) Define Experimental designs"),
                                            dbc.Form(children=[
                                                dbc.Col(children=[

                                                    dbc.FormText(
                                                        "Allows to link each file to its type/group to separate them self.approprietly afterwards."
                                                    ),
                                                    __typeGroupLink
                                                    ,
                                                    html.Br(),
                                                    dbc.FormText(
                                                        "Experimental Designs."
                                                    ),
                                                    dbc.Card(id="setted_classes_container", children=[html.P("No experimental design setted yet.")], style={"display": "block", "padding": "1em"}),
                                                    dbc.FormText(
                                                        "Define labels and filter out samples."
                                                    ),
                                                    __labelDefinition
                                                    ,
                                                ]),

                                            ]),
                                        ])

        __posNegPairing = html.Div(
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

        __posPattern = html.Div(
            [
                dbc.Input(id="distinct_id_pos_samples",
                          className="form_input_text",
                          placeholder="Pattern for positive samples"),
            ],
        )

        __negPattern = html.Div(
            [
                dbc.Input(id="distinct_id_neg_samples",
                          className="form_input_text",
                          placeholder="Pattern for negative samples"),
            ],
        )

        __otherPairing = html.Div(
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

        _type1Pattern = html.Div(
            [
                dbc.Input(id="distinct_id_1_samples",
                          className="form_input_text",
                          placeholder="Pattern for type 1 of samples"),
            ],
        )

        _type2Pattern = html.Div(
            [
                dbc.Input(id="distinct_id_2_samples",
                          className="form_input_text",
                          placeholder="Pattern for type 2 of samples"),
            ],
        )

        _dataFusion = html.Div(className="title_and_form", children=[
            html.H4(id="sep_samples_title", children="C) Data Fusion"),
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

        __sampleProportion = html.Div([
            dbc.Label(
                "Proportion of samples in test"),
            dbc.Input(
                id="in_percent_samples_in_test",
                value="0.2",
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
                value="25",
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
                                 dcc.Download(id="download-save-file")
                                 ])


    def _registerCallbacks(self) -> None:

        @self.app.callback(
            Output('upload_datatable_button', 'style'),
            [Input('upload_datatable', 'contents')],
            [State('upload_datatable', 'filename'),
             State("in_use_raw", "value")
             ]
        )
        def upload_data(list_of_contents, list_of_names, use_raw):
            if list_of_contents is not None:
                print("---> len list_of_names")
                print(len(list_of_names))
                print(list_of_names)
                print("---> content")
                print(len(list_of_contents))
                print(list_of_contents[:50])

                self.metabo_controller.set_data_matrix_from_path(list_of_names,
                                                                 data=list_of_contents,
                                                                 use_raw=use_raw)
                return dash.no_update
            else:
                return dash.no_update

        @self.app.callback(
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

        # @self.app.callback(
        #     Output('upload_metadata_button', 'style'),
        #     [Input('upload_metadata', 'contents')],
        #     [State('upload_metadata', 'filename'),
        #
        #      ]
        # )
        # def upload_metadata(list_of_contents, list_of_names):
        #     if list_of_contents is not None:
        #         self.metabo_controller.set_data_matrix_from_path(list_of_names,
        #                                                          data=list_of_contents,
        #                                                          )
        #         return dash.no_update

        @self.app.callback([Output("in_target_col_name", "options"),
                            Output("in_ID_col_name", "options"),
                            Output("output_in_case_of_error_in_path_to_metadata", "children")],
                           [Input('upload_metadata', 'contents')],
                           [State('upload_metadata', 'filename'),

                            ]
                           )
        def get_metadata_cols_names_to_choose_from(list_of_contents, list_of_names):
            if list_of_contents is not None:
                if self.metabo_controller.set_metadata(list_of_names, data=list_of_contents):
                    formatted_columns = self.metabo_controller.get_formatted_columns()
                    return formatted_columns, formatted_columns, ""
                else:
                    return [], [], "There is a problem, the format of your metadata file might not be supported. You " \
                                   "need to give either a .csv, .xlsX or .odX (where X replace variation of format). Ex: " \
                                   "file.xlsx, file.odt "
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
             Output("output_btn_add_desgn_exp", "children")],
            [Input("in_target_col_name", "value")],
        )
        def update_possible_classes_exp_design(target_col):
            if target_col != 0:
                self.metabo_controller.set_target_column(target_col)
                formatted_possible_targets = self.metabo_controller.get_formatted_unique_targets()
                return formatted_possible_targets, formatted_possible_targets, ""
            else:
                return [], [], ""

        @self.app.callback(
            [Output("class1_name", "value"),
             Output("possible_groups_for_class1", "value"),
             Output("class2_name", "value"),
             Output("possible_groups_for_class2", "value"),
             Output("setted_classes_container", "children"),
             Output("setted_classes_container", "style")],
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
                self.metabo_controller.add_experimental_design({c1: g1, c2: g2})
                return "", 0, "", 0, self._get_wrapped_experimental_designs(), {"display": "block", "padding": "1em"}
            else:
                return dash.no_update

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
            Output('output_button_split_file', 'children'),
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
             State("in_normalization", "value"),
             State("in_pairing_pos_neg", "value"),
             State("distinct_id_pos_samples", "value"),
             State("distinct_id_neg_samples", "value"),
             State("in_pairing_samples", "value"),
             State("distinct_id_1_samples", "value"),
             State("distinct_id_2_samples", "value"),
             ]
        )
        def saving_params_of_splits_batch(n, name_of_the_file, use_raw, nbr_splits, nbr_processes, #path_data_files,
                                          peakT, percent_in_test, autoOpt,  ID_col_name,#path_to_metadata,
                                          targets_col_name,
                                          type_of_processing, peak_pick, align, normalize, pair_pn, pair_id_pos,
                                          pair_id_neg, pair_12, pair_id_1, pair_id_2):
            """
            Create the file (json) which will contains all info about the split creation / data experiment.
            """
            if n >= 1:
                self.metabo_controller.set_id_column(ID_col_name)
                self.metabo_controller.set_splits_parameters(int(nbr_splits), float(percent_in_test))

                Utils.dump_metabo_expe(self.metabo_controller._metabo_experiment)

                return "The parameters file is created, the splits's creation should start shortly..."
            else:
                return dash.no_update

    def _get_wrapped_experimental_designs(self):
        children_container = [html.Div("Experimental design")]
        for name, full_name in self.metabo_controller.all_experimental_designs_names():
            button = dbc.Button("🞬", id=name, className="btn btn-secondary",
                                style={"color": "grey", "font-size": "medium"})
            # TODO: add callback for button
            children_container.append(html.Div(children=["- " + full_name, button],
                                               style={"display": "flex",
                                                      "justify-content": "space-between", "align-items": "center"}))
        return children_container

    # def parse_contents(self, contents, filename):
    #     content_type, content_string = contents.split(',')
    #
    #     decoded = base64.b64decode(content_string)
    #     try:
    #         if 'csv' in filename:
    #             # Assume that the user uploaded a CSV file
    #             df = pd.read_csv(
    #                 io.StringIO(decoded.decode('utf-8')))
    #         elif 'xls' in filename:
    #             # Assume that the user uploaded an excel file
    #             df = pd.read_excel(io.BytesIO(decoded))
    #     except Exception as e:
    #         print(e)
    #         return html.Div([
    #             "There was an error processing this file. Can't detect if there is the csv or xls file extension."
    #         ])
    #
    #     return df

