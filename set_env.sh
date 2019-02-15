#!/usr/bin/env bash

export PATH="/anaconda3/bin:$PATH"
conda create -n tableau python=3.5
conda install -n tableau --yes --file requirements.txt
while read requirement; do conda install -n tableau --yes $requirement; done < requirements.txt
conda env export --name tableau | grep -v "^prefix: " > environment_Mac.yml
source activate tableau
pip install --upgrade pip
pip install PyPDF2
pip install .
ipython kernel install --user --name=tableau
