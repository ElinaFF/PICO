from abc import abstractmethod
import dash_bootstrap_components as dbc

from dash import Dash


class MetaTab:
    def __init__(self, app: Dash):
        self.app = app
        self._registerCallbacks()

    @abstractmethod
    def getLayout(self) -> dbc.Tab:
        pass

    @abstractmethod
    def _registerCallbacks(self) -> None:
        pass
