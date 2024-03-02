FROM python:3.10-alpine

ADD ScannerSW.py product.py ./

RUN pip install paho-mqtt requests mysql-connector-python

CMD ["python", "./ScannerSW.py"]
