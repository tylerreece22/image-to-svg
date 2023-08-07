import io
import unittest

import pytest

from flask_app import app


class TestPageLoad(unittest.TestCase):
    def test_page_load(self):
        client = app.test_client()

        # Send a GET request to the route
        response = client.get("/")

        # Check if the response status code is 200 (OK)
        assert response.status_code == 200
        assert (
            response.data
            == b"\n    <!doctype html>\n    <title>Upload new File</title>\n    <h1>Upload new File</h1>\n    <form method=post enctype=multipart/form-data>\n      <input type=file name=file>\n      <input type=submit value=Upload>\n    </form>\n    "
        )

class TestPostFile(unittest.TestCase):
    def test_reject_if_file_not_in_request(self):
        client = app.test_client()

        # Send a GET request to the route
        response = client.post("/")

        # Check if the response status code is 200 (OK)
        assert response.status_code == 500

    def test_reject_if_file_has_invalid_extension(self):
        client = app.test_client()

        file_name = "fake-text-stream.txt"
        data = {
            'image': (io.BytesIO(b"some initial text data"), file_name)
        }
        # Send a GET request to the route
        response = client.post("/", data=data)

        # Check if the response status code is 200 (OK)
        assert response.status_code == 500

    @pytest.mark.skip(reason="need to come back to this one")
    def test_redirect_on_success(self):
        client = app.test_client()

        image = "pizza-cat.jpg"
        data = {
            'image': (open(image, 'rb'), image)
        }
        # Send a GET request to the route
        response = client.post("/", data=data)

        print(response.data)
        # Check if the response status code is 200 (OK)
        assert response.status_code == 200


if __name__ == "__main__":
    unittest.main()
