import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.decomposition import PCA
import umap



class Plots():
    def __init__(self, colors, y_train_true: list, y_train_pred: list, y_test_true: list, y_test_pred: list):
        self.colors = colors

    def show_algo_comparison_by_heatmap(self):
        return

    def _produce_UMAP_2D(self, X: pd.DataFrame):
        x = X.to_numpy()
        umap_2d = umap.UMAP(n_components=2, init='random', random_state=13)
        return umap_2d.fit_transform(x)

    def show_umap_2D(self, X: pd.DataFrame):
        umap_data = self._produce_UMAP_2D(X)
        fig_2d = px.scatter(
            umap_data, x=0, y=1,
            color=self.colors,
            labels={'color': 'Classes'}
        )
        return fig_2d.show()

    def _produce_PCA(self, X: pd.DataFrame):
        x = X.to_numpy()
        pca = PCA(n_components=2)
        return pca.fit_transform(x)

    def show_PCA(self, X: pd.DataFrame):
        pca_data = self._produce_PCA(X)
        fig = px.scatter(pca_data, x=0, y=1, color=self.colors)
        return fig.show()

    def show_accuracy_all(self, df):
        """
        plot the accuracy for each split on train and test set
        df : generated from Results.produce_accuracy_plot_all()
        """
        if "splits" not in df.columns:
            raise RuntimeError("To show the global accuracies plot, the dataframe needs to have a 'splits' column")
        if "accuracies" not in df.columns:
            raise RuntimeError("To show the global accuracies plot, the dataframe needs to have a 'accuracies' column")
        if "color" not in df.columns:
            raise RuntimeError("To show the global accuracies plot, the dataframe needs to have a 'color' column")

        fig = px.line(df, x='splits', y='accuracies', color='color', markers=True)
        return fig.show()

    def show_exp_info_all(self, df: pd.DataFrame):
        """
        display in table the number of samples, per classes, in train/test, etc.
        df : generated from Results.produce_info_expe()
        """
        if "stats" not in df.columns:
            raise RuntimeError("To show the global accuracies plot, the dataframe needs to have a 'stats' column")
        if "numbers" not in df.columns:
            raise RuntimeError("To show the global accuracies plot, the dataframe needs to have a 'numbers' column")

        fig = go.Figure(
            data=[go.Table(
                cells=dict(values=[df.stats, df.numbers]))
                ])
        return fig.show()

    def show_features_selection(self, df: pd.DataFrame):
        """
        table of features used by all models (all split of an algorithm)
        ranked by most used first
        only display 10 most or used in at least 75%? of models ?
        df : generated from Results.produce_features_importance_table()
        """
        if "features" not in df.columns:
            raise RuntimeError("To show the global accuracies plot, the dataframe needs to have a 'features' column")
        if "times_used" not in df.columns:
            raise RuntimeError("To show the global accuracies plot, the dataframe needs to have a 'times_used' column")
        if "importance_usage" not in df.columns:
            raise RuntimeError("To show the global accuracies plot, the dataframe needs to have a 'importance_usage' column")

        fig = go.Figure(
            data=[go.Table(
                header=dict(values=list(df.columns)),
                cells=dict(values=[df.features, df.times_used, df.importance_usage]))
            ])
        return fig.show()


    def show_split_metrics(self):
        """
        display in table the number of samples, per classes, in train/test, etc. for one split
        """
        return

    def show_metabolite_levels(self):
        """
        Plot in boxplot (with a dropdown to select the metabolite, max of N? metabolite)
        And show the intensity of this metabolite/ this feature in each class (one box per class)
        """
        return