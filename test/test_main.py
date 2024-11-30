import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_read_root():
    assert 2 == 2