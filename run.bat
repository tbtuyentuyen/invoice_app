@echo off
set INVOICE_APP_PATH=E:/workspace/invoice_app
set CONFIG_PATH=%INVOICE_APP_PATH%/data/config.json
set SHOP_INFO_PATH=%INVOICE_APP_PATH%/data/shop_info.json
python %INVOICE_APP_PATH%/main.py
