import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
import pandas as pd
import plotly.graph_objs as go

from LearnConfig import LEARN_CONFIG

resultsLayout = dbc.Tab(className="global_tab",
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
                                                label="Global results",
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
                                                label="Specific results",
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
                        ])