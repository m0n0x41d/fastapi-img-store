import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app


@pytest.fixture()
def client():
    return TestClient(app)


@patch("app.routes.main.minio")
def test_upload_file(mock_minio, client: TestClient) -> None:
    mock_minio.put_object.return_value = 'custom_image_id'

    test_file = 'tests/test.jpg'
    with open(test_file, 'rb') as f:
        files = {"file": ('test.jpeg', f, 'multipart/form-data')}
        response = client.post('/images/', files=files)

    response_json = response.json()
    assert response.status_code == 201
    assert response_json["message"] == "Image Uploaded OK"
    assert "ID" in response_json


def test_upload_no_file(client: TestClient) -> None:
    response = client.post('/images/', files=None)
    assert response.status_code == 400
    assert response.json() == {"detail": "No file provided"}


# still irrelevant — minio always return 200 on deletes
# def test_delete_file():
#     response = client.delete(f"/images/qwerty_lol_no_such_file")
#     assert response.status_code == 404
