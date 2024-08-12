import pytest
from fastapi.testclient import TestClient
from main import app
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Create a test client
client = TestClient(app)

def test_download_images_valid():
    response = client.post("/download-images/", json={"number_of_images": 3})
    assert response.status_code == 200
    assert "message" in response.json()
    assert "Se han guardado" in response.json()["message"]

def test_download_images_invalid_number():
    response = client.post("/download-images/", json={"number_of_images": -1})
    assert response.status_code == 400
    assert "Número de imágenes debe ser mayor a 0" in response.json()["detail"]

def test_download_images_no_images():
    response = client.post("/download-images/", json={"number_of_images": 0})
    assert response.status_code == 400
    assert "Número de imágenes debe ser mayor a 0" in response.json()["detail"]

def test_lambda_function_valid(event, context):
    # Mocking boto3 client for testing purposes
    s3_mock = boto3.client('s3', region_name='us-east-1')

    # Mock responses
    s3_mock.put_object = lambda Bucket, Key, Body: None  # Mock put_object to avoid actual S3 operations

    response = lambda_handler(event, context)

    assert response['statusCode'] == 200
    assert "Se han guardado" in json.loads(response['body'])

def test_lambda_function_invalid(event, context):
    response = lambda_handler({'number_of_images': -1}, context)

    assert response['statusCode'] == 400
    assert "Número de imágenes debe ser mayor a 0" in json.loads(response['body'])

@pytest.fixture
def event():
    return {
        'number_of_images': 2
    }

@pytest.fixture
def context():
    return {}

# Tests for first part
# import unittest
# from unittest.mock import patch, MagicMock
# import requests
# from main import download_image

# class TestMain(unittest.TestCase):

#     @patch('main.requests.get')
#     @patch('main.insert_url')
#     def test_download_image_success(self, mock_insert_url, mock_requests_get):
#         # Mocking the API response
#         mock_api_response = MagicMock()
#         mock_api_response.json.return_value = {'message': 'http://example.com/image.jpg'}
#         mock_requests_get.side_effect = [mock_api_response, MagicMock(status_code=200, content=b'image_data')]

#         with patch('main.open', unittest.mock.mock_open()) as mock_open:
#             download_image(1)
#             mock_requests_get.assert_called()
#             mock_insert_url.assert_called_once_with('http://example.com/image.jpg')
#             mock_open.assert_called_once_with('images/image_1.jpg', 'wb')
#             mock_open().write.assert_called_once_with(b'image_data')

#     @patch('main.requests.get')
#     def test_download_image_failure(self, mock_requests_get):
#         # Mocking a failed API request
#         mock_requests_get.side_effect = requests.exceptions.RequestException("Network error")
#         with self.assertRaises(requests.exceptions.RequestException):
#             download_image(1)

# if __name__ == '__main__':
#     unittest.main()
