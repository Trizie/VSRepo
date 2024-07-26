FROM python:latest

ADD ScannerSW.py product.py dbclass.py ./

RUN pip install Requirements.txt

CMD ["python", "./ScannerSW.py"]
