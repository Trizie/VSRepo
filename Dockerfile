FROM python:3.11

WORKDIR /usr/src

COPY ScannerSW.py product.py dbclass.py ./

RUN pip install --no-cache-dir --requirement Requirements.txt

CMD ["python", "./ScannerSW.py"]
