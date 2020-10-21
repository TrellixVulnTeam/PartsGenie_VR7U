#!/usr/bin/env python3
"""
Created on March 17 2020

@author: Melchior du Lac
@description: Parts Genie

"""
import argparse
import tempfile
import os
import logging
import shutil
import docker


def main(server_url,
         output,
         inputfile,
         input_format,
         taxonomy_input,
         taxonomy_format):
    """The docker of the client to call the PartsGenie service

    :param server_url: The ip address of the Pars Genie REST instance
    :param output: The path to the output file
    :param inputfile: The path to the input file
    :param input_format: The input type of the gile. Suported input: tar, sbml
    :param taxonomy_input: The taxonomy id
    :param taxonomy_format: The format of the taxonomy id. Valid options: json, str

    :type server_url: str
    :type output: str
    :type inputfile: str
    :type input_format: str
    :type taxonomy_input: str
    :type taxonomy_format: str

    :rtype: bool
    :return: The success or failure of the function
    """
    docker_client = docker.from_env()
    image_str = 'brsynth/partsgenie-standalone'
    try:
        image = docker_client.images.get(image_str)
    except docker.errors.ImageNotFound:
        logging.warning('Could not find the image, trying to pull it')
        try:
            docker_client.images.pull(image_str)
            image = docker_client.images.get(image_str)
        except docker.errors.ImageNotFound:
            logging.error('Cannot pull image: '+str(image_str))
            exit(1)
    with tempfile.TemporaryDirectory() as tmpOutputFolder:
        if os.path.exists(inputfile):
            shutil.copy(inputfile, tmpOutputFolder+'/input.dat')
            if taxonomy_input=='json':
                shutil.copy(taxonomy_input, tmpOutputFolder+'/taxonomy_input.dat')
                command = ['python /home/tool_PartsGenie.py',
                           '-server_url',
                           str(server_url),
                           '-input',
                           '/home/tmp_output/input.dat',
                           '-input_format',
                           str(input_format),
                           '-taxonomy_input',
                           '/home/tmp_output/taxonomy_input.dat',
                           '-taxonomy_format',
                           str(taxonomy_format),
                           '-output',
                           '/home/tmp_output/output.dat']
            else:
                command = ['python /home/tool_PartsGenie.py',
                           '-server_url',
                           str(server_url),
                           '-input',
                           '/home/tmp_output/input.dat',
                           '-input_format',
                           str(input_format),
                           '-taxonomy_input',
                           str(taxonomy_input),
                           '-taxonomy_format',
                           str(taxonomy_format),
                           '-output',
                           '/home/tmp_output/output.dat']
            container = docker_client.containers.run(image_str,
                                                     command,
                                                     detach=True,
                                                     stderr=True,
                                                     volumes={tmpOutputFolder+'/': {'bind': '/home/tmp_output', 'mode': 'rw'}})
            container.wait()
            err = container.logs(stdout=False, stderr=True)
            err_str = err.decode('utf-8')
            if 'ERROR' in err_str:
                print(err_str)
            elif 'WARNING' in err_str:
                print(err_str)
            if not os.path.exists(tmpOutputFolder+'/output.dat'):
                print('ERROR: Cannot find the output file: '+str(tmpOutputFolder+'/output.dat'))
            else:
                shutil.copy(tmpOutputFolder+'/output.dat', output)
            container.remove()
        else:
            logging.error('Cannot find one or more of the input file: '+str(inputfile))
            exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser('Convert the results of RP2 and rp2paths to SBML files')
    parser.add_argument('-server_url', type=str)
    parser.add_argument('-output', type=str)
    parser.add_argument('-input', type=str)
    parser.add_argument('-input_format', type=str)
    parser.add_argument('-taxonomy_input', type=str)
    parser.add_argument('-taxonomy_format', type=str)
    params = parser.parse_args()
    main(params.server_url,
         params.output,
         params.input,
         params.input_format,
         params.taxonomy_input,
         params.taxonomy_format)
