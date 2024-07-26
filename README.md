# Vorratsschrank - Scannersoftware

![Build Status](https://github.com/Trizie/VSRepo/actions/workflows/super-linter/badge.svg)

![Build Status](https://github.com/Trizie/VSRepo/actions/workflows/python-app.yml/badge.svg)

[![Python 3.9](https://img.shields.io/badge/Python-3.11-green.svg)](https://shields.io/)

Programm für die Organisation eines Vorratsschranks

Ein Arduino wurde mit Scannermodul ausgestattet. Ein Wippschalter am Arduino ermöglicht es zwischen Lösch- und Speichermodus zu wechseln.
Per mqtt-Protokoll wird der Barcode des gescannten Produkts an ein Python-Programm gesendet.
Über API wird der Produktname ermittelt und das Produkt wird in einer mysql-Datenbank (über SSH-Tunnel an host pythonanywhere) gespeichert.
Auf einer Homepage (flask & bootstrap, host pythonanywhere) wird der Inhalt des Vorratsschranks dargestellt.
