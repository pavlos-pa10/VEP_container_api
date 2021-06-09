# API for running VEP container to annotate uploaded VCF file

This API requires two main components. A Flask REST API and the docker image for VEP. 
Please follow the installation steps below to install these two main components. 

# Installation

## Part 1 of 2
## VEP docker installation and setup
1. Install docker for your operating system from here: ([Get Docker | Docker Documentation](https://docs.docker.com/get-docker/)
2. Pull the vep image and create cache directory
`docker pull ensemblorg/ensembl-vep`
`mkdir $HOME/vep_data`
`chmod a+rwx $HOME/vep_data`

3. Install the reference genome (human genome) databases and the available plugins in your local --cache directory. This will take a while but it is best to install these prior to running the API and the files are needed to run VEP for annotation. 
`docker run -t -i -v $HOME/vep_data:/opt/vep/.vep ensemblorg/ensembl-vep perl INSTALL.pl -a cfp -s homo_sapiens -y GRCh38 -g all`
