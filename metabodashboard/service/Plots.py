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

    #TODO : faire la sauvegarde dans results des resultats de heatmap pour pouvoir sortir la figure
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
        #TODO : sort data by times_used or importance, and take only top 10-20 to display

        fig = go.Figure(
            data=[go.Table(
                header=dict(values=list(df.columns)),
                cells=dict(values=[df.iloc[:10, :].features, df.iloc[:10, :].times_used,
                                   df.iloc[:10, :].importance_usage]))
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

# def show_info_exp ancienne
#with open("testest", "r") as conf_file:
#    splits_config = json.load(conf_file)

#splits_dict = splits_config["Splits"]
#nbr_in_train = len(splits_dict["split0"][0])
#nbr_in_test = len(splits_dict["split0"][1])
#nbr_tot = nbr_in_train + nbr_in_test
#classes_train = splits_dict["split0"][2]
#classes_tot = classes_train.extend(splits_dict["split0"][3])
#count_per_class = Counter(classes_tot)

#row1 = html.Tr([html.Td("Total number of samples"), html.Td(str(nbr_tot))])
#row2 = html.Tr([html.Td("Number of samples in train"), html.Td(str(nbr_in_train))])
#row3 = html.Tr([html.Td("Number of samples in test"), html.Td(str(nbr_in_test))])
## row4 = html.Tr([html.Td(list(count_per_class.keys())[0]), html.Td("Astra")])

#table_body = [html.Tbody([row1, row2, row3])]
#table = dbc.Table(table_body, id="table_exp_info", borderless=True, hover=True)