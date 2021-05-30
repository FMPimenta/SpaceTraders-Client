#!/usr/bin/python
# -*- coding: utf-8 -*-

#username: TheLegendaryTrader
#token: 736730b1-cfee-4ce4-a20d-872861782934

from os.path import isfile
import sqlite3
import requests
import json

URL = "https://api.spacetraders.io"

#Functions
def getStatus ():
    r = requests.get('%s/game/status' % URL)
    content = json.loads(r.content.decode())
    print(content["status"])

# Programa principal
print("Booting SpaceTraders client terminal...")
getStatus()

print("Are you a registered member of the SpaceTraders? Y/N")
registered = input("")

if registered == "N":
    print("Commencing account creation protocol...")
    print("What would you like to be called?")
    username = input("")

    print("Welcome to the SpaceTraders, %s!" % username)

    print("Requesting acess token from mainframe...")
    r = requests.post("%s/users/%s/claim" % (URL, username))
    content = json.loads(r.content.decode())
    print(content)
    token = content["token"]
    print("%s, your standard issue token is: %s" % (username, token))
    print("Please save this token in a safe external memory device, as losing it means termination of access to your SpaceTraders account")
