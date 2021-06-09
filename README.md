# API for running VEP container to annotate uploaded VCF file



## Description
This Flask API allows the user to upload a VCF file to the server. Once the VCF file is uploaded a call to 
the docker container of ensemblorg/ensembl-vep is made with the uploaded VCF file as input. \
Once the VEP execution ends, the resulting annotation is parsed into json format and returned as a json response
through the flask API to the user. \

## Getting Started
This API requires two main components. A Flask REST API and the docker image for VEP. \
Please follow the installation steps below to install these two main components. 

## Main Dependencies
`Python 3` Tested with Python 3.9\
`Flask`\
Docker image: `ensemblorg/ensembl-vep:latest`\

## Installation

### Part 1 of 2: VEP docker installation and local cache databases setup
1. Install docker for your operating system from here: ([Get Docker | Docker Documentation](https://docs.docker.com/get-docker/)\
2. Pull the vep image and create cache directory\
`docker pull ensemblorg/ensembl-vep`\
`mkdir $HOME/vep_data`\
`chmod a+rwx $HOME/vep_data`\

3. Install the reference genome (human genome) databases and the available plugins in your local --cache directory. This will take a while but it is best to install these prior to running the API and the files are needed to run VEP for annotation. \
`docker run -t -i -v $HOME/vep_data:/opt/vep/.vep ensemblorg/ensembl-vep perl INSTALL.pl -a cfp -s homo_sapiens -y GRCh38 -g all`

### Part 2 of 2 : Flask and python dependencies


## API execution examples using curl

## Testing 
The tests and the coverage of the code can be viewed by running:
`pytest --cov=project`

## Authors
`Pavlos Antoniou @pavlos-pa10`