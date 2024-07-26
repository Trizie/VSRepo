FROM python:3.11

WORKDIR /usr/src

COPY ScannerSW.py product.py dbclass.py send_barcode.py ./

RUN pip install --no-cache-dir --requirement Requirements.txt

CMD ["python", "./ScannerSW.py"]
CMD ["python", "./send_barcode.py"]