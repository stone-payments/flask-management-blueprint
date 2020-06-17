import pytest


@pytest.fixture(scope="package")
def test_app():
    from flask import Flask
    app = Flask(__name__)
    return app
