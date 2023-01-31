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

def getCredentials(sessionKey):
    myapp = 'TA_Scipted_Input_PassEnrypt'
    #log(myapp)
    try:
        entities = entity.getEntities(['admin', 'passwords'], namespace=myapp,owner='nobody', sessionKey=sessionKey)
        #log(entities)
    except Exception as e:
        raise Exception("Could not get %s credentials from splunk. Error: %s" % (myapp, str(e)))
    for i, c in entities.items():
        log("Username: "+str(c['username']))
        if c['username'] == "admin":
            log("Username: "+str(c['username']))
            log("Clear Password: "+str(c['clear_password']))
            log("------------------------------------------")
            return c['clear_password']
        raise Exception("No credentials have been found")  


def main():
    sessionKey = sys.stdin.readline().strip()
    #log(sessionKey)
    if len(sessionKey) == 0:
        log("Error - Did not receive a session key from splunkd.Please enable passAuth in inputs.conf")
        exit(2)
    api_key = getCredentials(sessionKey)
    #log("api_key_clear_text: "+str(api_key))
if __name__ == "__main__":
    main()
