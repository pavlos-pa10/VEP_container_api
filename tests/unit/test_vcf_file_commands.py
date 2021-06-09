"""
This file contains the functional tests for the app.py file regarding the VCF file upload 
"""

from app import app
import io
from io import BytesIO

def test_get_upload_vcf_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/upload' page is requested - GET
    THEN check the response is valid and the upload page is returned
    """
    response = test_client.get('/api/upload')
    assert response.status_code == 200
    assert b'Upload VCF file for VEP annotation.' in response.data
    

def test_post_upload_file(test_client,tmpdir):
    """
    GIVEN a Flask application 
    WHEN the '/upload' page is posted to (POST) with a vcf file
    THEN check that the responose is 302 user is redirected to the '/index' page
    """
    data = {
       
        'file': (BytesIO(b'FILE CONTENT'), 'test.vcf')
    }
    response=test_client.post('/api/upload', 
    content_type="multipart/form-data",
    data=data,
    follow_redirects=True
    )

    assert response.status_code == 200
    

    
def test_post_upload_file_not_vcf(test_client):
    """
    GIVEN a Flask application 
    WHEN the '/upload' page is posted to (POST) with a file that is not a .vcf
    THEN check that message it is not allowed returned to user
    """
    data = {
       
        'file': (BytesIO(b'FILE CONTENT'), 'test.txt')
    }
    response=test_client.post('/api/upload', 
    content_type="multipart/form-data",
    data=data,
    follow_redirects=True
    )

    assert response.status_code == 200
    assert b'You must select a valid VCF file' in response.data


