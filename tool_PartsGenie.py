#!/usr/bin/env python3

"""
Created on Feburary 25 2020

@author: Melchior du Lac
@description: Galaxy script to query PartsGenie REST service

"""

import argparse
import sys
import tempfile
import tarfile
import glob
import logging
import json
import os

sys.path.insert(0, '/home/')
import rpTool

##
#
#
if __name__ == "__main__":
    parser = argparse.ArgumentParser('Python wrapper to call PartsGenie')
    parser.add_argument('-server_url', type=str)
    parser.add_argument('-output', type=str)
    parser.add_argument('-input', type=str)
    parser.add_argument('-input_format', type=str)
    parser.add_argument('-taxonomy_input', type=str)
    parser.add_argument('-taxonomy_format', type=str)
    params = parser.parse_args()
    tax_id = -1
    ##### taxonomy #######
    if params.taxonomy_format=='json':
        tax_id = None
        with open(params.taxonomy_input, 'r') as ti:
            tax_dict = json.load(ti)
            tax_id = int(tax_dict['taxonomy'][0])
    elif params.taxonomy_format=='string':
        tax_id = int(params.taxonomy_input)
    else:
        logging.error('Taxonomy input format not recognised')
        exit(1)
    if params.input_format=='tar':
        client = rpTool.PartsGenieClient(params.server_url)
        with tempfile.TemporaryDirectory() as tmpInputFolder:
            with tarfile.open(params.input) as rf:
                rf.extractall(tmpInputFolder)
            in_files = glob.glob(tmpInputFolder+'/*')
            #write the tar
            with tarfile.open(params.output, mode='w:xz') as ot:
                for sbol in in_files:
                    with tempfile.TemporaryDirectory() as tmpOutputFolder:
                        client.run(sbol, tax_id, tmpOutputFolder)
                        outSBOL = glob.glob(tmpOutputFolder+'/*')
                        if len(outSBOL)>1:
                            logging.warning('There are more than one item in the output folder: '+str(outSBOL))
                            logging.warning('Skipping this file: '+str(sbol))
                            continue
                        elif len(outSBOL)==0:
                            logging.warning('PartsGenie did not return any results: '+str(sbol))
                            continue
                        info = tarfile.TarInfo(str(sbml_path.split('/')[-1]))
                        info.size = os.path.getsize(outSBOL[0])
                        ot.addfile(tarinfo=info, fileobj=open(outSBOL[0], 'rb'))
    elif params.input_format=='sbol':
        client = rpTool.PartsGenieClient(params.server_url)
        with tempfile.TemporaryDirectory() as tmpOutputFolder:
            client.run(params.input, tax_id, tmpOutputFolder)
            outSBOL = glob.glob(tmpOutputFolder+'/*')
            if len(outSBOL)>1:
                logging.error('There are more than one item in the output folder: '+str(outSBOL))
                exit(1)
            elif len(outSBOL)==0:
                logging.error('PartsGenie did not return any results')
                exit(1)
            with open(outSBOL[0], 'r') as r:
                with open(params.output, 'w') as s:
                    s.write(r.read())
    else:
        logging.error('Input format not detected: '+str(params.input_format))
        exit(1) 
