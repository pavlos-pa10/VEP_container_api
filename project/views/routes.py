'''
09.06.2021
'''
from . import views_blueprint
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from flask import current_app, render_template, request, session, flash, redirect, url_for,jsonify
import click
import os
import docker
import shlex
import json
import re

from project import views





'''
ROUTES 
'''

#Index page
@views_blueprint.route('/')
def index():
    print (current_app.config['UPLOAD_FOLDER'])
    return render_template('views/index.html')

#About page
@views_blueprint.route('/about')
def about():
    
    return render_template('views/about.html')

# GET Upload form and on submit POST vcf file and run VEP container
@views_blueprint.route('/api/upload', methods = ['GET', 'POST'])
def  upload():
    if request.method == 'GET':
        return render_template('views/upload.html')
    if request.method == 'POST':
      f = request.files['file']
      print(f.filename)
      if not check_extension(f.filename):
          flash("You must select a valid VCF file")
          return redirect(url_for('views.index'))
      else:
        
        f.save(os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        vcf_file=f.filename 
        session['vcf_file']=vcf_file
        client=start_docker_vep_container()
        run_vep_docker(client,vcf_file)
        parse_vep_output(current_app.config['UPLOAD_FOLDER']+"/annotation_vep.txt")
        return redirect(url_for('views.api_annotations'))
        


@views_blueprint.route('/annotations', methods = ['GET'])
def view_annotations():
    current_app.config['JSON_SORT_KEYS'] = False
    parse_vep_output(current_app.config['UPLOAD_FOLDER']+"/annotation_vep.txt")
    json_file=current_app.config['UPLOAD_FOLDER']+"/vep_output.json"
    data = json.load(open(json_file))
    flash(f"Dockerized VEP results ")
    print(jsonify(data).json)
    mydata=jsonify(**data, sort_keys=False).json
    return render_template('views/annotations.html', jsonfile=mydata)

@views_blueprint.route('/api/annotations', methods = ['GET'])
def api_annotations():
    current_app.config['JSON_SORT_KEYS'] = False
    json_file=current_app.config['UPLOAD_FOLDER']+"/vep_output.json"
    data = json.load(open(json_file))
    return jsonify(data)

"""
HELPER FUNCTIONS
"""

#Start docker client
def start_docker_vep_container():
    client=docker.from_env()
    return client

#Helper function to check vcf extension of input file
def check_extension(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

#Helper function to generate the command to run VEP 
def generate_docker_command(vcf_file):
    vep_path=current_app.config['VEP_PATH']
    home_path=current_app.config['UPLOAD_FOLDER']
    command= shlex.split("perl vep --cache --offline --format vcf --force_overwrite --input_file " + vep_path+"/"+vcf_file +" --output_file " + vep_path +"/annotation_vep.txt ")
    return command


# Run VEP container image with the command generated, detach=False to wait for it to finish and remove=True to remove image after execution
def run_vep_docker(client,file_location):
    command=generate_docker_command(file_location)
    volumes={current_app.config['UPLOAD_FOLDER'] : {'bind': current_app.config['VEP_PATH'], 'mode': 'rw'}}
    container=client.containers.run('ensemblorg/ensembl-vep', command, volumes=volumes, detach=False, remove=True)
    return container
    
# Parse VEP output to produce json format to be returned from API
def parse_vep_output(vcf_file):
    version=""
    run_date=""
    json_dict={}
    results=[]
    headers_list=[]
    results_list=[]
    
    f=open(current_app.config['UPLOAD_FOLDER']+"/annotation_vep.txt", 'r')
   
    for line in f:
        line=line.rstrip()
        if line.startswith("## "):
            pattern = 'ENSEMBL VARIANT EFFECT PREDICTOR (.*)'
            match = re.search(pattern, line) 
            if match:
                version=match.group(1)
                print(version)
            pattern="Output produced at (.*)"
            match = re.search(pattern, line) 
            if match:
                run_date=match.group(1)
                print(run_date)
        elif line.startswith('#Uploaded_variation'):
            headers=line.split("\t")
            print(headers)
            headers_list=headers
        else:
            results_list=line.split("\t")
            res = {headers_list[i]: results_list[i] for i in range(len(headers_list))}
            loc=res["Location"]
            chromosome=loc.split(":")[0]
            start=loc.split(":")[1]
            end=start
            res["Location"]={
            "chromosome":chromosome,
            "start":start,
            "end":end
            }
            results.append(res)
            #print(res)
        json_dict['VEP_version']=version
        json_dict['run_date']=run_date
        json_dict['results']=results

        with open(current_app.config['UPLOAD_FOLDER']+"/vep_output.json", "w") as outfile: 
            json.dump(json_dict, outfile, sort_keys = False, indent = 4, separators = (',', ': '))
    
    
