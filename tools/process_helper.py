""" Process helper module """


import os
import subprocess

MONGOD_EXE = os.environ['MONGOD_EXE']
DB_PATH = os.environ['DB_PATH']

def start_broker():
    """ Start MongoDB Broker """
    cmd = f'"{MONGOD_EXE}" --dbpath "{DB_PATH}"'
    subprocess.Popen(
        cmd,
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

def stop_broker():
    """ Stop MongoDB Broker """
    cmd = 'taskkill /F /IM mongod.exe'
    subprocess.Popen(
        cmd,
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
