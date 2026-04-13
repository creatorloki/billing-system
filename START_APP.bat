@echo off
cd /d "%~dp0"
echo Starting College Project: Billing System...
py -m pip install flask
cd src
py app.py
pause