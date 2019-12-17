from main import create_application
import pytest

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_application()
    testing_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()
    yield testing_client
    ctx.pop()

def test_hoi(test_client):
    response = test_client.get('/blabla')
    assert response == 'bla'
