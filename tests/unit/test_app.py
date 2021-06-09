from tests.unit.test_docker_commands import test_start_docker_client
from app import app
import os
import os.path
from flask import current_app

app_ctx = app.app_context()
app_ctx.push()

def test_index_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'Welcome to the Web API for VEP!' in response.data
    assert b'Created by Pavlos Antoniou' in response.data

def test_about_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    
    response = test_client.get('/about')
    assert response.status_code == 200
    assert b'This API allows the user to upload a VCF file.' in response.data


def test_api_annotations(test_client):
    """
    GIVEN a Flask application
    WHEN the '/api/annotations' page has been requested  (GET) 
    THEN check the response displays the resulting json containing the vcf file annotations 
        and that it has content by checking if the response json contains the VEP_version key
    """
    response = test_client.get('/api/annotations')
    assert response.status_code ==200
    assert response.json['VEP_version'] 