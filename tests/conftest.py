import pytest
from duckquest.graph.logic import GraphLogic
from duckquest.graph.manager import GraphManager


class DummyGameManager:
    def __init__(self, difficulty=11):
        self.difficulty = difficulty
        self.graph = GraphManager()
        self.graph.assign_weights_and_colors(self.difficulty)


@pytest.fixture
def logic():
    """Fixture for initializing GraphLogic with a dummy game manager."""
    game_manager = DummyGameManager()
    return GraphLogic(game_manager)
