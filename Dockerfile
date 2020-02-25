FROM python:3.7

WORKDIR /home/

ENV PYTHONPATH="$DIRPATH:$PYTHONPATH"

RUN pip install --upgrade pip
RUN pip install pySBOL
RUN pip install requests[security]
RUN pip install sseclient==0.0.22

RUN apt-get update
RUN apt-get install git

RUN git clone https://github.com/neilswainston/PartsGenieClient.git

RUN mv PartsGenieClient/parts_genie/client.py /home/rpTool.py
