import sys,os
import json
import requests as req
import splunk.entity as entity
import datetime
import string
import random
import re

def format_time():
    t = datetime.datetime.now()
    s = t.strftime('%m-%d-%Y %H:%M:%S.%f')
    return s[:-3]

def log(message):
    with open(os.path.join(os.environ['SPLUNK_HOME'], 'var/log/splunk', 'TA_Scipted_Input_PassEnrypt.log'), 'a') as f:
        f.write(format_time() + " -0000 " + message + "\n")

def getCredentials(sessionKey,username):
    myapp = 'TA_Scipted_Input_PassEnrypt'
    try:
        entities = entity.getEntities(['admin', 'passwords'], namespace=myapp,owner='nobody', sessionKey=sessionKey)
    except Exception as e:
        raise Exception("Could not get %s credentials from splunk. Error: %s" % (myapp, str(e)))
    for i, c in list(entities.items()):
        if c['username'] == username:
            return c['clear_password']

def main():
    sessionKey = sys.stdin.readline().strip()
    if len(sessionKey) == 0:
        log("Error - Did not receive a session key from splunkd.Please enable passAuth in inputs.conf")
        exit(2)
    Username = "Henry"
    password = getCredentials(sessionKey,Username)
    log("Username: "+str(Username))
    log("Password: "+str(password))

if __name__ == "__main__":
    main()
