@echo off
set INVOICE_APP_PATH=
set CONFIG_PATH=%INVOICE_APP_PATH%/dataconfig.json
set SHOP_INFO_PATH=%INVOICE_APP_PATH%/data/shop_info.json
set BUYER_INFO_PATH=%INVOICE_APP_PATH%/data/buyer_info.json
python %INVOICE_APP_PATH%/main.py
