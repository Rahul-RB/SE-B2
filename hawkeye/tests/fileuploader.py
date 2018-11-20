#!/usr/bin/env python
from flask import Flask, Request, request
from io import BytesIO
import unittest

RESULT = False

class TestFileFail(unittest.TestCase):

    def test_1(self):

        class FileObj(BytesIO):
            
            def close(self):
                print('in file close')
                global RESULT
                RESULT = True
        
        class MyRequest(Request):
            def _get_file_stream(*args, **kwargs):
                return FileObj()

        app = Flask(__name__)
        app.debug = True
        app.request_class = MyRequest

        @app.route("/upload", methods=['POST'])
        def upload():
            f = request.files['file']
            print('in upload handler')
            self.assertIsInstance(
                f.stream,
                FileObj,
            )
            f.close()
            return 'ok'

        client = app.test_client()
        resp = client.post(
            '/upload',
            data = {
                'file': (BytesIO(f.filename)),
            }
        )
        self.assertEqual(
            'ok',
            resp.data,
        )
        global RESULT
        self.assertTrue(RESULT)


if __name__ == '__main__':
    unittest.main()