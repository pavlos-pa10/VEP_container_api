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
Python 3 Tested with Python 3.9\
Flask\
Docker image: `ensemblorg/ensembl-vep:latest`

## Installation

### Part 1 of 2: VEP docker installation and local cache databases setup
1. Install docker for your operating system from here: ([Get Docker | Docker Documentation](https://docs.docker.com/get-docker/)\
2. Pull the vep image and create cache directory\
```
docker pull ensemblorg/ensembl-vep
mkdir $HOME/vep_data
chmod a+rwx $HOME/vep_data
```

3. Install the reference genome (human genome) databases and the available plugins in your local --cache directory. This will take a while but it is best to install these prior to running the API and the files are needed to run VEP for annotation. \
```
docker run -t -i -v $HOME/vep_data:/opt/vep/.vep ensemblorg/ensembl-vep perl INSTALL.pl -a cfp -s homo_sapiens -y GRCh38 -g all
```
### Part 2 of 2 : Install Flask and python dependencies
```
mkdir vep_api
cd vep_api
git init
git pull https://github.com/pavlos-pa10/VEP_container_api.git
python3 -m venv venv 
source venv/bin/activate
pip install -r requirements.txt
```

## Execution
After finishing the above installation steps run the flask server from within the vep_api directory created in the installation process above:

```
cd vep_api
flask run
```

Go to `http://127.0.0.1:5000/` or `http://localhost:5000/` \
Click on VCF_upload from navigation menu. This will take you to `http://localhost:5000/api/upload` \
Select a VCF file from your computer or select the example vcf within the repository in the directory `./test_vcf/homo_sapiens_GRCh38.vcf` \

Click Submit. This will post your VCF to server and upload it for VEP. The VEP container starts running with this input VCF. \
Wait until the VEP container completes and the annotations will be presented as json in the same window at `http://localhost/api/annotations`.\
Do not refresh or leave the window after pressing Submit while VEP is running. \
If you do leave the window or close it by accident, you can still find the annotations after a few minutes at:\
`http://localhost/api/annotations`


## API execution examples using curl
From the same directory (vep_api):

### Upload VCF - POST
```
curl -F "file=@test_vcf/homo_sapiens_GRCh38.vcf" http://127.0.0.1:5000/api/upload
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>Redirecting...</title>
<h1>Redirecting...</h1>
<p>You should be redirected automatically to target URL: <a href="/api/annotations">/api/annotations</a>. If not click the link.
```
# View annotations - GET
```
curl http://127.0.0.1:5000/api/annotations

{"VEP_version":"v104.3","run_date":"2021-06-09 18:09:13","results":[{"#Uploaded_variation":"rs7289170","Location":{"chromosome":"22","start":"17181903","end":"17181903"},"Allele":"G","Gene":"ENSG00000093072","Feature":"ENST00000262607","Feature_type":"Transcript","Consequence":"synonymous_variant","cDNA_position":"1571","CDS_position":"1359","Protein_position":"453","Amino_acids":"Y","Codons":"taT/taC","Existing_variation":"-","Extra":"IMPACT=LOW;STRAND=-1"},{"#Uploaded_variation":"rs7289170","Location":{"chromosome":"22","start":"17181903","end":"17181903"},"Allele":"G","Gene":"ENSG00000093072","Feature":"ENST00000330232","Feature_type":"Transcript","Consequence":"synonymous_variant","cDNA_position":"841","CDS_position":"636","Protei...}
```
## Testing 
The tests and the coverage of the code can be viewed by running:
`pytest --cov=project`

## Authors
`Pavlos Antoniou @pavlos-pa10`