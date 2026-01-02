@echo off
set INVOICE_APP_PATH=E:/workspace/invoice_app
set CONFIG_PATH=%INVOICE_APP_PATH%/data/config.json
set SHOP_INFO_PATH=%INVOICE_APP_PATH%/data/shop_info.json

set MONGOD_EXE=c:/Users/Tuyen/OneDrive/Documents/mongo_database/mongodb-windows-x86_64-8.2.1/mongodb-win32-x86_64-windows-8.2.1/bin/mongod.exe
set DB_PATH=C:/Users/Tuyen Tuyen/mongo_database
python %INVOICE_APP_PATH%/main.py
