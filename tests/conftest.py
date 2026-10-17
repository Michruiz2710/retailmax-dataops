"""base sintetica nueva para cada sesion."""

import pytest

from scripts.create_db import create_db
from src.extract import extract_data


@pytest.fixture(scope="session")
def db_path(tmp_path_factory):
    return create_db(str(tmp_path_factory.mktemp("datos") / "ventas.db"))


@pytest.fixture
def ventas(db_path):
    return extract_data(db_path)
