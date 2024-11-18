import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import html

from ..conf import parameters as cfg


class Plots:
    def __init__(self, colors: str):
        self.colors = colors
        self.__default_stylesheet_for_cooc = [
            {
                "selector": "node",
                "style": {
                    "width": "mapData(size, 0, 1, 5, 50)",
                    "height": "mapData(size, 0, 1, 5, 50)",
                    "content": "data(label)",
                    'text-background-color': 'white',  # Set the background color for the text
                    'text-background-opacity': 1,  # Set the opacity of the text background
                    'text-background-padding': '2px',
                    "font-size": "6px",
                    "text-valign": "center",
                    "text-halign": "center",
                    'border-color': 'black',  # Set the border color
                    'border-width': '1px',  # Set the border width
                    'border-style': 'solid',  # Set the border style
                    'text-opacity': 0,
                    'background-color': '#00143E',
                }
            },
            {
                "selector": "edge",
                "style": {
                    "width": "mapData(size, 0, 1, 1, 5)",
                    'line-color': 'gray',
                }
            }
        ]

    # TODO : faire la sauvegarde dans results des resultats de heatmap pour pouvoir sortir la figure
    def show_algo_comparison_by_heatmap(self):
        return

    # def show_two_most_important_feature(self, data, classes, algo):
    #     f1name = data.iloc[0, 0]
    #     f2name = data.iloc[1, 0]
    #     fig = px.scatter(
    #         data,
    #         x=f1name,
    #         y=f2name,
    #         color=classes,
    #         color_continuous_scale=self.colors,
    #         title="",
    #     )
    #
    #     fig.update_layout(
    #         {
    #             "plot_bgcolor": "rgba(0, 0, 0, 0)",
    #             "paper_bgcolor": "rgba(0, 0, 0, 0)",
    #         },
    #         title="Top 2"
    #         + " features selected by "
    #         + algo,
    #     )
    #     return fig

    def show_umap(self, umap_data, classes, algo, slider_value, sample_ids: list):
        val = [5, 10, 40, 100, "used", "all"]
        fig = px.scatter(
            umap_data,
            x=0,
            y=1,
            color=classes,
            color_continuous_scale=self.colors,
            title="",
            hover_name=sample_ids,
        )

        fig.update_layout(
            {
                "plot_bgcolor": "rgba(0, 0, 0, 0)",
                "paper_bgcolor": "rgba(0, 0, 0, 0)",
            },
            title="UMAP applied on top "
                  + str(val[slider_value])
                  + " features selected by "
                  + algo,
        )
        return fig

    def show_3D_umap(self, umap_data, classes, algo, slider_value, sample_ids: list):
        val = [5, 10, 40, 100, "used", "all"]
        fig = px.scatter_3d(
            umap_data,
            x=0,
            y=1,
            z=2,
            color=classes,
            color_continuous_scale=self.colors,
            title="",
            hover_name=sample_ids,
        )

        fig.update_layout(
            {
                "plot_bgcolor": "rgba(0, 0, 0, 0)",
                "paper_bgcolor": "rgba(0, 0, 0, 0)",
            },
            title="UMAP applied on top "
                  + str(val[slider_value])
                  + " features selected by "
                  + algo,
        )
        return fig

    def show_PCA(self, pca_data, pca_labels, classes, slider_value, algo, sample_ids: list):
        val = [5, 10, 40, 100, "used", "all"]
        fig = px.scatter(
            pca_data,
            labels=pca_labels,
            x=0,
            y=1,
            color=classes,
            color_continuous_scale=self.colors,
            title="",
            hover_name=sample_ids,
        )
        fig.update_layout(
            {
                "plot_bgcolor": "rgba(0, 0, 0, 0)",
                "paper_bgcolor": "rgba(0, 0, 0, 0)",
            },
            title="PCA applied on top "
                  + str(val[slider_value])
                  + " features selected by "
                  + algo,
        )
        return fig

    def show_3D_PCA(self, pca_data, pca_labels, classes, slider_value, algo, sample_ids: list):
        val = [5, 10, 40, 100, "used", "all"]
        fig = px.scatter_3d(
            pca_data,
            labels=pca_labels,
            x=0,
            y=1,
            z=2,
            color=classes,
            color_continuous_scale=self.colors,
            title="",
            hover_name=sample_ids,
        )
        fig.update_layout(
            {
                "plot_bgcolor": "rgba(0, 0, 0, 0)",
                "paper_bgcolor": "rgba(0, 0, 0, 0)",
            },
            title="PCA applied on top "
                  + str(val[slider_value])
                  + " features selected by "
                  + algo,
        )
        return fig

    def show_general_confusion_matrix(self, cm, labels, text, algo, split):
        # labels = ["0", "1"]

        fig = go.Figure(
            data=go.Heatmap(
                # labels=dict(x="Prediciton", y="Vérité", color="Nombre de prédictions"),
                z=cm,
                x=labels,
                y=labels,
                # text=text,
                colorscale=self.colors,
                showscale=False
                # texttemplate="%{text}",
            )
        )
        fig = fig.update_traces(text=text, texttemplate="%{text}", hovertemplate=None)
        fig.update_layout(
            title="Confusion matrix of split " + str(split) + " by " + algo,
            xaxis_title="Prediciton",
            yaxis_title="Truth",
        )

        # fig = px.imshow(
        #         cm,
        #         labels=dict(x="Prediciton", y="Vérité", color="Nombre de prédictions"),
        #         x=list(set(labels)),
        #         y=list(set(labels)),
        #         color_continuous_scale=self.colors,
        #         text_auto=True
        # )
        # fig.update_traces(text=text)
        return fig

    def show_accuracy_all(self, df, algo):
        """
        plot the accuracy for each split on train and test set
        df : generated from Results.produce_accuracy_plot_all()
        """
        if "splits" not in df.columns:
            raise RuntimeError(
                "To show the global accuracies plot, the dataframe needs to have a 'splits' column"
            )
        if "accuracies" not in df.columns:
            raise RuntimeError(
                "To show the global accuracies plot, the dataframe needs to have a 'accuracies' column"
            )
        if "color" not in df.columns:
            raise RuntimeError(
                "To show the global accuracies plot, the dataframe needs to have a 'color' column"
            )

        fig = px.bar(df, x="splits", y="accuracies", color="color", barmode="group")

        fig.update_yaxes(range=[0, 1.1])
        fig.update_layout(
            {
                "plot_bgcolor": "rgba(246, 247, 247, 0.4)",
                "paper_bgcolor": "rgba(0, 0, 0, 0)",
            }
        )
        return fig

    def show_exp_info_all(self, df: pd.DataFrame):
        """
        display in table the number of samples, per classes, in train/test, etc.
        df : generated from Results.produce_info_expe()
        """
        if "stats" not in df.columns:
            raise RuntimeError(
                "To show the global accuracies plot, the dataframe needs to have a 'stats' column"
            )
        if "numbers" not in df.columns:
            raise RuntimeError(
                "To show the global accuracies plot, the dataframe needs to have a 'numbers' column"
            )

        # fig = go.Figure(
        #     data=[go.Table(
        #         cells=dict(values=[df.stats, df.numbers]))
        #         ])

        row1 = html.Tr([html.Td(df.iloc[0, 0]), html.Td(df.iloc[0, 1])])
        row2 = html.Tr([html.Td(df.iloc[1, 0]), html.Td(df.iloc[1, 1])])
        row3 = html.Tr([html.Td(df.iloc[2, 0]), html.Td(df.iloc[2, 1])])
        row4 = html.Tr([html.Td(df.iloc[3, 0]), html.Td(df.iloc[3, 1])])
        table_body = [html.Tbody([row1, row2, row3, row4])]
        return table_body

    def show_features_selection(self, df: pd.DataFrame, algo):
        """
        table of features used by all models (all split of an algorithm)
        ranked by most used first
        only display 10 most or used in at least 75%? of models ?
        df : generated from Results.produce_features_importance_table()
        """
        if "features" not in df.columns:
            raise RuntimeError(
                "To show the global accuracies plot, the dataframe needs to have a 'features' column"
            )
        if "times_used" not in df.columns:
            raise RuntimeError(
                "To show the global accuracies plot, the dataframe needs to have a 'times_used' column"
            )
        if "importance_usage" not in df.columns:
            raise RuntimeError(
                "To show the global accuracies plot, the dataframe needs to have a 'importance_usage' column"
            )
        # TODO : sort data by times_used or importance, and take only top 10-20 to display

        fig = go.Figure(
            data=[
                go.Table(
                    header=dict(values=list(df.columns), align="center"),
                    cells=dict(
                        values=[
                            df.iloc[:10, :].features,
                            df.iloc[:10, :].times_used,
                            df.iloc[:10, :].importance_usage,
                        ],
                        align="center",
                    ),
                )
            ]
        )
        fig.update_layout(
            title="Table of top 10 features sorted by importance for " + algo
        )
        fig.update_layout(title="Table of top 10 features sorted by importance")
        return fig

    def show_split_metrics(self):
        """
        display in table the number of samples, per classes, in train/test, etc. for one split
        """
        return

    def show_metabolite_levels(self, features_data, algo, sample_name: list):
        """
        Plot in stripchart (boxplot with point and no box)
        (with a dropdown to select the metabolite, max of N? metabolite)
        And show the intensity of this metabolite/ this feature in each class (one box per class)
        """
        if features_data.shape[1] > cfg.max_used_features_to_show:
            fig = generate_empty_figure("Features used is to large to be shown.")
            return fig

        df_container = []
        for c in features_data.columns:
            if c != "targets":
                df_container.append(pd.DataFrame({
                    "features_name": [c] * len(features_data["targets"]),
                    "intensity": list(features_data[c]),
                    "targets": list(features_data["targets"]),
                    "sample_name": sample_name,
                }))
        
        df_aggregated = pd.concat(df_container, ignore_index=True)

        # ----> for violin plot
        # fig = go.Figure()
        #
        # fig.add_trace(
        #     go.Violin(
        #         x=df_dup["features_name"][df_dup["targets"]=="NA"],
        #         y=df_dup["intensity"][df_dup["targets"]=="NA"],
        #         legendgroup='Yes', scalegroup='Yes', name='NA',
        #         side='negative',
        #     )
        # )
        #
        # fig.add_trace(
        #     go.Violin(
        #         x=df_dup["features_name"][df_dup["targets"] == "Med"],
        #         y=df_dup["intensity"][df_dup["targets"] == "Med"],
        #         legendgroup='Yes', scalegroup='Yes', name='Med',
        #         side='positive',
        #     )
        # )
        #
        # fig.update_traces(meanline_visible=True,
        #                   # points='all',  # show all points
        #                   # jitter=0.05,  # add some jitter on points for better visibility
        #                   # scalemode='count'
        #                   )
        # fig.update_layout(violingap=0, violinmode='overlay')
        # ---> end for violin plot

        fig = px.strip(
            df_aggregated,
            x="features_name",
            y="intensity",
            color="targets",
            title="Abundance of {} in each sample by class for {}".format("all",
                                                                          # feature,
                                                                          algo
                                                                          ),
            hover_name="sample_name",
        )

        fig.update_layout(
            {
                "plot_bgcolor": "rgba(0, 0, 0, 0)",
                "paper_bgcolor": "rgba(0, 0, 0, 0)",
            }
        )
        return fig

    def show_heatmap_wrong_samples(self, data_train, data_test, samples_names, algos):
        fig = go.Figure()
        fig.add_trace(
            go.Heatmap(
                z=data_test, x=algos, y=samples_names, opacity=1, colorscale="Reds"
            )
        )
        fig.update_layout(
            title="Number of wrong prediction per sample in test sets for all splits"
        )

        return fig

    def show_heatmap_features_usage(self, df, importance_threshold):
        fig = go.Figure()
        fig.add_trace(
            go.Heatmap(
                z=df.values, x=df.columns, y=df.index, opacity=1, colorscale="blues"
            )
        )
        importance_threshold = round(importance_threshold, 3)
        fig.update_layout(title=f"Mean importance of features (>{importance_threshold}) for all splits")
        return fig

    def show_barplot_comparaison_algo(self, algos, train_acc, train_std, test_acc, test_std):
        fig = go.Figure(data=[
            go.Bar(name='Train', x=algos, y=train_acc, error_y=dict(type='data', array=train_std)),
            go.Bar(name='Test', x=algos, y=test_acc, error_y=dict(type='data', array=test_std))
        ])
        # Change the bar mode
        fig.update_layout(barmode='group')
        return fig

    def show_2d(self, data, classes, sample_names):
        return px.scatter(
            data,
            x=data.columns[0],
            y=data.columns[1],
            color=classes,
            color_continuous_scale=self.colors,
            title="",
            hover_name=sample_names,
        )

    def show_3d(self, data, classes, sample_names):
        return px.scatter_3d(
            data,
            x=data.columns[0],
            y=data.columns[1],
            z=data.columns[2],
            color=classes,
            color_continuous_scale=self.colors,
            title="",
            hover_name=sample_names,
        )

    @staticmethod
    def get_train_test_split_graph(nbr_element, slider_value, percent_test):
        m_element = nbr_element
        k_test = int(percent_test * m_element)

        def choose(k, n):
            if n > k:
                return 0
            if n < 0:
                return 0
            if k < 0:
                return 0
            a = 1
            b = 1
            for i in range(1, n + 1):
                a = a * i
                b = b * (k - i + 1)
            return b / a

        def f(i, j):
            return choose(m_element - i, j - i) * choose(i, k_test - (j - i)) / choose(m_element, k_test)

        M = np.zeros((m_element, m_element))
        for a in range(1, m_element + 1):
            for b in range(1, m_element + 1):
                M[a - 1, b - 1] = f(a, b)

        V = np.zeros(m_element)
        V[k_test] = 1
        nbr_limit = 100
        valeurs = np.zeros(nbr_limit)

        for c in range(nbr_limit):
            valeurs[c] = V[m_element - 1]
            V = np.matmul(V, M)

        def threshold_at_99(selected):
            vector = np.zeros(m_element)
            vector[k_test] = 1
            for i in range(selected - 1):
                vector = np.matmul(vector, M)
            result = 0
            for i in range(m_element):
                result += vector[m_element - i - 1]
                if result > 0.9999:
                    return int((m_element - i - 1) / m_element * 100)

        fig = px.scatter(y=valeurs, x=[i for i in range(1, len(valeurs) + 1)],
                    labels={'x': 'Number of splits',
                            'y': 'Probability a'},
                         )
        fig.add_trace(go.Scatter(x=[slider_value], y=[valeurs[slider_value - 1]], mode='markers',
                                 marker_symbol='circle',
                                 marker_size=10))
        fig.add_annotation(x=slider_value, y=valeurs[slider_value - 1],
                           text=f"({slider_value} splits, a={valeurs[slider_value - 1]:.2f}, b={threshold_at_99(slider_value)}%)",
                           showarrow=True, arrowhead=1)
        fig.update_layout(showlegend=False)
        return fig

    def get_default_stylesheet_for_cooc_graph(self):
        return self.__default_stylesheet_for_cooc

    def format_style_for_selected_node(self, node):
        return {
            "selector": 'node[id = "{}"]'.format(node['id']),
            'style': {
                'content': 'data(label)',
                'text-opacity': 1,
                'background-color': '#13BD00'
            }
        }

    def create_coocurence_graph(self, counter, mean_importance, number_of_split):
        def formatNode(node):
            return {'data': {'id': node, 'label': node, 'size': mean_importance[node]}}

        def formatEdge(edge):
            return {'data': {'source': edge[0], 'target': edge[1], 'size': counter[edge] / number_of_split}}

        seen_feature = set()
        dash_parameters = []
        for pair, weight in counter.items():
            x, y = pair
            if x not in seen_feature:
                dash_parameters.append(formatNode(x))
                seen_feature.add(x)
            if y not in seen_feature:
                dash_parameters.append(formatNode(y))
                seen_feature.add(y)
            dash_parameters.append(formatEdge(pair))

        return dash_parameters



def generate_empty_figure(text):
    # Create an empty figure
    fig = go.Figure()

    # Add annotation
    fig.add_annotation(
        text=text,
        xref="paper", yref="paper",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=20)
    )

    # Update layout to remove axes and grid
    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False)
    )

    return fig