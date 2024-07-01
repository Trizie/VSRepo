# Vorratsschrank - Scannersoftware

![Build Status](https://github.com/Trizie/VorratsschrankRepo/actions/workflows/python-app.yml/badge.svg)

Programm für die Organisation eines Vorratsschranks

Ein Arduino wurde mit Scannermodul ausgestattet. Per mqtt-Protokoll wird der barcode des gescannten Produkts an ein Python-Programm geschickt. 
Über API wird der Produktname ermittelt und das Produkt wird in einer mysql-Datenbank (über SSH-Tunnel an host pythonanywhere) gespeichert.
Auf einer website (flask & bootstrap, host pythonanywhere) wird der Inhalt des Vorratsschranks dargestellt. 
