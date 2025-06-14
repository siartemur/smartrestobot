import pytest
from fastapi.testclient import TestClient
from app.main import app

import sys
import os

# 'app' klasörünü Python path'ine ekle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))



@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c