import plotly.express as px
import plotly.graph_objects as go


class Plots():
    def __init__(self, colors, y_train_true: list, y_train_pred: list, y_test_true: list, y_test_pred: list):
        self.colors = colors

    def show_algo_comparison_by_heatmap(self):
        return

    def show_umap_2D(self, umap_data):
        fig_2d = px.scatter(
            umap_data, x=0, y=1,
            color=self.colors,
            labels={'color': 'Classes'}
        )
        return fig_2d.show()

    def show_PCA(self, pca_data):
        fig = px.scatter(pca_data, x=0, y=1, color=self.colors)
        return fig.show()

    def show_accuracy_all(self):
        """
        plot the accuracy for each split on train and test set
        """
        return

    def show_exp_info_all(self):
        """
        display in table the number of samples, per classes, in train/test, etc.
        """
        return

    def show_features_selection(self):
        """
        table of features used by all models (all split of an algorithm)
        ranked by most used first
        only display 10 most or used in at least 75%? of models ?
        """
        return


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