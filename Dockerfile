FROM python:latest

COPY ScannerSW.py product.py dbclass.py ./

RUN pip install Requirements.txt

CMD ["python", "./ScannerSW.py"]
