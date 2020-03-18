# PartsGenie

SBOL implementation of PartsGenie

## Getting Started

This is a docker galaxy tools, and thus, the docker needs to be built locally where Galaxy is installed. 

## Input

Required information:
* **-input**: (string) Path to the input file
* **-input_format**: (string) Format of the input (tar or sbol)
* **-taxonomy_input**: (string) Either string or path to json file
* **-taxonomy_format**: (string) Format of the input format (string or json)
* **-server_url**: (string) IP address of PartsGenie

## Output

* **output**: (string) Path to the tar or sbol output

## Prerequisites

* Base Docker Image: [python:3.7](https://hub.docker.com/_/python)

## Installing

To build the image using the Dockerfile, use the following command:

```
docker build -t brsynth/partsgenie-standalone .
```

### Running the tests

To run the test, untar the test.tar.xz file and run the following command:

```
python run.py -input test/input.sbol -input_format sbol -taxonomy_input 8333 taxonomy_format string -output test/test_output.sbol
```

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

v0.1

## Authors

* **Melchior du Lac**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Thomas Duigou
* Joan Hérisson

### How to cite rpOptBioDes?
