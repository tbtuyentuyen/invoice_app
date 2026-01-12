@echo off
set INVOICE_APP_HOME=E:/workspace/invoice_app/home
set INVOICE_APP_PATH=E:/workspace/invoice_app
set CONFIG_DIR=%INVOICE_APP_HOME%/user_data

set MONGOD_EXE=c:/Users/Tuyen/OneDrive/Documents/mongo_database/mongodb-windows-x86_64-8.2.1/mongodb-win32-x86_64-windows-8.2.1/bin/mongod.exe
set DB_PATH=C:/Users/Tuyen Tuyen/mongo_database
python %INVOICE_APP_PATH%/main.py
