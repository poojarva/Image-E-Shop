import pytest
from flask import Flask

app = Flask(__name__)

@pytest.fixture
def client():

    #app.config['TESTING'] = True
    client = app.test_client()

    yield client