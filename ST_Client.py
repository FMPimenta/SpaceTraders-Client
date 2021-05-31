#!/usr/bin/python
# -*- coding: utf-8 -*-

#username: TheLegendaryTrader
#token: 736730b1-cfee-4ce4-a20d-872861782934

#ship id: ckpd45efh19150216s6cnqldmvt

#username: FrankySnow3000
#token: cbf3684b-6667-44c1-817f-e14dc581bab9

#Imports
import requests
import json
#------------------------------------------------------------------------------------------------

#Globals
URL = "https://api.spacetraders.io"
#------------------------------------------------------------------------------------------------

#Classes
class SpaceTradersClientTerminal:
    
    def __init__(self, token):
        self.token = token  #Bearer + token
        self.accountStatus()

    def accountStatus(self):
        print("Loading account status...")
        r = requests.get("%s/my/account" % URL, headers={'Authorization': token})
        content = json.loads(r.content.decode())
        self.username = content["user"]["username"]
        print("Here is your account status, " + self.username)
        content = json.loads(r.content.decode())
        print(content["user"])

    def browseLoans(self):
        print("Loading available loans...")
        r = requests.get("%s/types/loans" % URL, headers={'Authorization': token})
        print("Here are all available loans for you to take, " + self.username)
        content = json.loads(r.content.decode())
        print(content["loans"])

    def takeLoan(self, type):
        loanType = type
        parameters = {"type": loanType}
        print("")

        print("Processing loan...")
        r = requests.get("%s/my/loans" % URL, headers={'Authorization': token}, params=parameters)
        
        while (r.status_code == 422):
            print("Loan type invalid, please insert a valid loan type: ")
            loanType = input("")
            parameters = {"type": loanType}
            print("")

            print("Processing loan...")
            r = requests.get("%s/my/loans" % URL, headers={'Authorization': token}, params=parameters)

        print("Loan sucessfully taken, here is the corresponding info:")
        content = json.loads(r.content.decode())
        print(content)

#------------------------------------------------------------------------------------------------

#Main code
print("Booting SpaceTraders client terminal...")
r = requests.get('%s/game/status' % URL)
content = json.loads(r.content.decode())
print(content["status"])

print("Are you a registered member of the SpaceTraders? Y/N")
registered = input("")
print("")

if registered == "N":
    print("Commencing account creation protocol...")
    print("What would you like to be called?")
    username = input("")
    print("")

    print("Welcome to the SpaceTraders, %s!" % username)
    print("")

    print("Requesting acess token from mainframe...")
    r = requests.post("%s/users/%s/claim" % (URL, username))

    while (r.status_code == 409):
        print("That name has been claimed, please insert a different one")
        username = input("")
        print("")

        print("Requesting acess token from mainframe...")
        r = requests.post("%s/users/%s/claim" % (URL, username))

    content = json.loads(r.content.decode())
    token = "Bearer " + content["token"]
    print("%s, your standard issue token is: %s" % (username, token))
    print("Please save this token in a safe external memory device, as losing it means termination of access to your account")
    print("")
else: #Y
    print("Commencing user validation protocol...")
    print("Please insert your access token")
    token = "Bearer " + input("")
    print("")

    print("Validating...")
    r = requests.get("%s/my/account" % URL, headers={'Authorization': token})

    while (r.status_code == 401):
        print("Invalid token please refrain from inserting \"Bearer\" before the token as it is not necessary")
        print("Please insert a valid access token")
        token = "Bearer " + input("")
        print("")

        print("Validating...")
        r = requests.get("%s/my/account" % URL, headers={'Authorization': token})

    print("Access granted!")

terminal = SpaceTradersClientTerminal(token)

print("Insert your command: (EXIT to shutdown terminal and HELP for help)")
command = input("")
print("")

while (command != "EXIT"):
    if (command == "HELP"):
        print("I regret to inform that this terminal does not have a helpdesk module installed")
    elif (command == "BROWSE LOANS"): 
        terminal.browseLoans()
    elif (command[:9] == "TAKE LOAN"): #TAKE LOAN $TYPE
        terminal.takeLoan(command[10:])

    print("Insert your command: (EXIT to shutdown terminal and HELP for help)")
    command = input("")
    print("")
#------------------------------------------------------------------------------------------------
