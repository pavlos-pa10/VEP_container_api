"""
This file contains the functional tests for the app.py file regarding the docker container run
"""

from app import app
import os
import os.path
from project.views import routes
import io
from io import BytesIO
from flask import current_app

app_ctx = app.app_context()
app_ctx.push()

def test_start_docker_client(test_client):
    """
    GIVEN a Flask application with the docker pypi package installed 
    WHEN the docker client is started
    THEN check that a docker client is created successfully
    """
    client=routes.start_docker_vep_container()
    assert client

def test_generate_vep_run_arguments(test_client):
    """
    GIVEN an input VCF file and a  VEP container 
    WHEN generate_docker_command is run
    THEN the command for VEP is parsed and the list of arguments is returned
    """

    command=routes.generate_docker_command(vcf_file="test.vcf")

    assert isinstance(command,list)


def test_run_vep_container(test_client):
    """
    GIVEN a started VEP container client
    WHEN the docker image is run with input vcf file
    THEN the docker image is run and the output file exists at $UPLOAD_FOLDER ($VEP_PATH)
    """
    client=routes.start_docker_vep_container()
    vcf_file="test.vcf"
    home_path=current_app.config['UPLOAD_FOLDER']
    routes.run_vep_docker(client,vcf_file)
    assert os.path.isfile(home_path+"/annotation_vep.txt")