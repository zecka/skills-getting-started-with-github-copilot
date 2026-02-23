import copy
import pytest
from fastapi.testclient import TestClient

import src.app as app_module


@pytest.fixture()
def client():
    """Fournit un instance TestClient pour l'application FastAPI."""
    return TestClient(app_module.app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Restore a deep copy of `app_module.activities` before each test for isolation.

    Arrange: capture a deepcopy of the original activities.
    Act: yield to the test which may mutate `app_module.activities`.
    Assert: after the test, restore the original state.
    """
    original = copy.deepcopy(app_module.activities)
    yield
    app_module.activities = original
