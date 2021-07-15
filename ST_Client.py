#!/usr/bin/python
# -*- coding: utf-8 -*-

#01b79536-9550-4798-8375-11b18c0c5654

#TEST
#ae45d5d4-0e0f-4050-9195-cd4e3c6720b8

#Imports
import requests
import json
#------------------------------------------------------------------------------------------------

#Globals
URL = "https://api.spacetraders.io"
COMMANDS = ["ACCOUNT INFO", "BROWSE LOANS", "TAKE LOAN $TYPE", 
            "BROWSE SHIPS $SYSTEM", "BUY SHIP $LOCATION $TYPE", 
            "PURCHASE $SHIPID $GOODID $QUANTITY", "BROWSE MARKET $LOCATION", 
            "SCAN SYSTEM $SYSTEM"]
#------------------------------------------------------------------------------------------------

#Classes
class SpaceTradersClientTerminal:
    
    def __init__(self, token):
        self.token = token  #Bearer + token
        self.accountStatus()

    def requestHelp(self):
        print("Displaying all valid commands:")
        print("")
        for command in COMMANDS:
            print(command)
        print("")

    def accountStatus(self):
        print("Loading account status...")
        r = requests.get("%s/my/account" % URL, headers={'Authorization': self.token})
        content = json.loads(r.content.decode())
        self.username = content["user"]["username"]
        print("Here is your account status, " + self.username)
        content = json.loads(r.content.decode())
        print(content["user"])

    def browseLoans(self):
        print("Loading available loans...")
        r = requests.get("%s/types/loans" % URL, headers={'Authorization': self.token})
        print("Here are all available loans for you to take, " + self.username)
        content = json.loads(r.content.decode())
        print(content["loans"])

    def takeLoan(self, type):
        parameters = {"type": type}
        print("")

        print("Processing loan...")
        r = requests.get("%s/my/loans" % URL, headers={'Authorization': self.token}, params=parameters)
        
        while (r.status_code == 422):
            print("Loan type invalid, please insert a valid loan type: ")
            loanType = input("")
            parameters = {"type": loanType}
            print("")

            print("Processing loan...")
            r = requests.get("%s/my/loans" % URL, headers={'Authorization': self.token}, params=parameters)

        print("Loan sucessfully taken, here is the corresponding info:")
        print(r.content.decode())

    def browseShips(self, system):
        print("Loading ship listings in " + system)
        r = requests.get("%s/systems/%s/ship-listings" % (URL, system), headers={'Authorization': self.token})
        print("Here are all ships available for purchase, " + self.username)
        content = json.loads(r.content.decode())
        for ship in content["shipListings"]:
            print(ship)
            print("")

    def buyShip(self, location, type):
        parameters = {"location": location, "type": type}
        print("Processing purchase...")
        r = requests.get("%s/my/ships" % URL, headers={'Authorization': self.token}, params=parameters)    

        if (r.status_code == 422):
            print("Invalid purchase, please verify location and type of ship and try again")
            print("")
        else:
            print("Purchase successfull, " + self.username)
            content = json.loads(r.content.decode())
            print(content)
            #CONTENT NOT DISPLAYING PROPERLY

    def purchaseOrder(self, shipID, goodID, quantity):
        parameters = {"shipId": shipID, "good": goodID, "quantity":quantity}
        print("Placing purchase order...")
        r = requests.get("%s/my/purchase-orders" % URL, headers={'Authorization': self.token}, params=parameters)

        if (r.status_code == 422):
            print("Invalid purchase order, please verify shipID, good and quantity and try again")
            print("")
        else:
            print("Purchase successfull, " + self.username)
            content = json.loads(r.content.decode())
            print(content)

    def browseMarket(self, location):
        print("Downloading market data...")
        r = requests.get("%s/locations/%s/marketplace" % (URL,location), headers={'Authorization': self.token})
        
        if (r.status_code == 200):
            print("Market data obtained sucessfully:")
            content = json.loads(r.content.decode())
            print(content)
        else:
            print("Market data download failed")

    def scanSystem(self, system):
        print("Scanning system...")
        r = requests.get("%s/systems/%s/locations" % (URL, system), headers={'Authorization': self.token})

        if (r.status_code == 200):
            print("System scan complete:")
            content = json.loads(r.content.decode())
            print(content)
            print("")
        else:
            print("System scan failed, please verify the system symbol and try again")
            print("")

#------------------------------------------------------------------------------------------------

#Main code
print("Booting SpaceTraders client terminal...")
r = requests.get('%s/game/status' % URL)
content = json.loads(r.content.decode())
print(content["status"])

print("Are you a registered member of the SpaceTraders? Y/N")
registered = input("")
print("")

if (registered == "N"):
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
    print("%s, your standard issue token is: %s" % (username, content["token"]))
    print("Please save this token in a safe external memory device, as losing it means termination of access to your account")
    print("")
elif (registered == "Y"): #Y
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
command = input("").split()
print("")

while (command[0] != 'EXIT'):
    if (command == ["HELP"]):
        terminal.requestHelp()
    elif (command == ["ACCOUNT", "INFO"]):          #ACCOUNT INFO
        terminal.accountStatus()
    elif (command == ["BROWSE", "LOANS"]):          #BROWSE LOANS
        terminal.browseLoans()
    elif (command[:2] == ["TAKE", "LOAN"]):         #TAKE LOAN $TYPE
        terminal.takeLoan(command[2])
    elif (command[:2] == ["BROWSE", "SHIPS"]):      #BROWSE SHIPS $SYSTEM
        terminal.browseShips(command[2])
    elif (command[:2] == ["BUY", "SHIP"]):          #BUY SHIP $LOCATION $TYPE
        terminal.buyShip(command[2], command[3])
    elif (command[:1] == ["PURCHASE"]):             #PURCHASE $SHIPID $GOODID $QUANTITY
        terminal.purchaseOrder(command[2], command[3], command[4])
    elif (command[:2] == ["BROWSE", "MARKET"]):     #BROWSE MARKET $LOCATION
        terminal.browseMarket(command[2])
    elif (command[:2] == ["SCAN", "SYSTEM"]):       #SCAN SYSTEM $SYSTEM
        terminal.scanSystem(command[2])

    print("Insert your command: (EXIT to shutdown terminal and HELP for help)")
    command = input("").split()
    print("")
#------------------------------------------------------------------------------------------------
