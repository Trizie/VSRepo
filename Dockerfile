FROM python:3.10

ADD ScannerSW.py .

RUN pip install requests paho-mqtt

CMD ["python", "./ScannerSW.py"]
