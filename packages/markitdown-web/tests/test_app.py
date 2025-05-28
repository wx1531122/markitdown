import os
import pytest
from markitdown_web.app import app as flask_app
from io import BytesIO

@pytest.fixture
def app_fixture():
    flask_app.config.update({
        "TESTING": True,
        "SECRET_KEY": "testsecretkey",
        "WTF_CSRF_ENABLED": False,
    })
    upload_folder = os.path.join(flask_app.root_path, 'tmp_uploads')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    yield flask_app

@pytest.fixture
def client(app_fixture):
    return app_fixture.test_client()

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Upload File for Markdown Conversion" in response.data

def test_upload_no_file_part(client):
    response = client.post('/upload', data={})
    assert response.status_code == 302
    response = client.get(response.location)
    assert b"No file part" in response.data

def test_upload_empty_filename(client):
    data = {'file': (BytesIO(b""), '')}
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 302
    response = client.get(response.location)
    assert b"No selected file" in response.data

def test_upload_success(client):
    data = {'file': (BytesIO(b"Test content for markdown conversion."), 'test.txt')}
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert b"Conversion Result" in response.data
    assert b"Test content for markdown conversion." in response.data
    # The sample.txt created earlier is not used by this test directly,
    # but the upload functionality is tested.
    # The actual conversion logic is mocked/assumed to be handled by the `markitdown` library.
