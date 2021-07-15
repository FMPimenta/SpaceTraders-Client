#!/usr/bin/python
# -*- coding: utf-8 -*-

# Imports
import requests

# ------------------------------------------------------------------------------------------------

# Globals
URL = "https://api.spacetraders.io"

COMMANDS = ["ACCOUNT INFO", "BROWSE LOANS", "TAKE LOAN $TYPE",
            "BROWSE SHIPS $SYSTEM", "BUY SHIP $LOCATION $TYPE",
            "PURCHASE $SHIPID $GOODID $QUANTITY", "BROWSE MARKET $LOCATION",
            "SCAN SYSTEM $SYSTEM"]
# ------------------------------------------------------------------------------------------------

# Classes


class SpaceTradersClientTerminal:

    def __init__(self, token):
        self.token = token  # Bearer + token
        self.accountStatus()

    def requestHelp(self):
        print("Displaying all valid commands:")
        print("")

        for command in COMMANDS:
            print(command)

        print("")

    def accountStatus(self):
        print("Loading account status...")
        r = requests.get("%s/my/account" % URL, 
        headers={'Authorization': self.token})

        response = r.json()
        self.username = response["user"]["username"]

        print("Here is your account status, " + self.username)
        response = r.json()
        
        print(response["user"])

    def browseLoans(self):
        print("Loading available loans...")
        r = requests.get("%s/types/loans" % URL, 
        headers={'Authorization': self.token})

        print("Here are all available loans for you to take, " + self.username)
        response = r.json()

        print(response["loans"])

    def takeLoan(self, type):
        parameters = {"type": type}

        print("")
        print("Processing loan...")
        r = requests.post("%s/my/loans" % URL, 
        headers={'Authorization': self.token}, params=parameters)

        if (r.status_code != 201):
            print("Unable to take loan verify loan type and try again "
            "(only one loan can be active at any time)")
            print("")

        print("Loan sucessfully taken, here is the corresponding info:")
        response = r.json()

        print(response)

    def browseShips(self, system):
        print("Loading ship listings in " + system)
        r = requests.get("%s/systems/%s/ship-listings" % (URL, system), 
        headers={'Authorization': self.token})

        print("Here are all ships available for purchase, " + self.username)
        response = r.json()
        
        for ship in response["shipListings"]:
            print(ship)
            print("")

    def buyShip(self, location, type):
        parameters = {"location": location, "type": type}
        print("Processing purchase...")
        r = requests.post("%s/my/ships" % URL, 
        headers={'Authorization': self.token}, params=parameters)

        if (r.status_code != 201):
            print("Invalid purchase, please verify location and type of ship "
            "and try again")
            print("")
        else:
            print("Purchase successfull, " + self.username)
            response = r.json()
            print(response)
            # response NOT DISPLAYING PROPERLY

    def purchaseOrder(self, shipID, goodID, quantity):
        parameters = {"shipId": shipID, "good": goodID, "quantity": quantity}
        print("Placing purchase order...")
        r = requests.post("%s/my/purchase-orders" % URL,
        headers={'Authorization': self.token}, params=parameters)

        if (r.status_code != 200):
            print("Invalid purchase order, please verify shipID, good and "
            "quantity and try again")
            print("")
        else:
            print("Purchase successfull, " + self.username)
            response = r.json()
            print(response)

    def browseMarket(self, location):
        print("Downloading market data...")
        r = requests.get("%s/locations/%s/marketplace" % (URL, location), 
        headers={'Authorization': self.token})

        if (r.status_code == 200):
            print("Market data obtained sucessfully:")
            response = r.json()
            print(response)
        else:
            print("Market data download failed")

    def scanSystem(self, system):
        print("Scanning system...")
        r = requests.get("%s/systems/%s/locations" %
        (URL, system), headers={'Authorization': self.token})

        if (r.status_code == 200):
            print("System scan complete:")
            response = r.json()
            print(response)
            print("")
        else:
            print("System scan failed, please verify the system symbol "
            "and try again")
            print("")

# ------------------------------------------------------------------------------------------------


# Main code
print("Booting SpaceTraders client terminal...")
r = requests.get('%s/game/status' % URL)
response = r.json()
print(response["status"])

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

        print("Requesting access token from mainframe...")
        r = requests.post("%s/users/%s/claim" % (URL, username))

    response = r.json()
    token = "Bearer " + response["token"]
    print("%s, your standard issue token is: %s" %
          (username, response["token"]))

    print("Please save this token in a safe external memory device, as "
    "losing it means termination of access to your account")
    print("")

elif (registered == "Y"):  # Y
    print("Commencing user validation protocol...")
    print("Please insert your access token")
    token = "Bearer " + input("")
    print("")

    print("Validating...")
    r = requests.get("%s/my/account" % URL, headers={'Authorization': token})

    while (r.status_code == 401):
        print("Invalid token please refrain from inserting \"Bearer\" before "
        "the token as it is not necessary")

        print("Please insert a valid access token")
        token = "Bearer " + input("")
        print("")

        print("Validating...")
        r = requests.get("%s/my/account" %
                         URL, headers={'Authorization': token})

    print("Access granted!")

terminal = SpaceTradersClientTerminal(token)

print("Insert your command: (EXIT to shutdown terminal and HELP for help)")
command = input("").split()
print("")

while (command[0] != 'EXIT'):

    if (command == ["HELP"]):
        terminal.requestHelp()
    elif (command == ["ACCOUNT", "INFO"]):  # ACCOUNT INFO
        terminal.accountStatus()
    elif (command == ["BROWSE", "LOANS"]):  # BROWSE LOANS
        terminal.browseLoans()
    elif (command[:2] == ["TAKE", "LOAN"]):  # TAKE LOAN $TYPE
        terminal.takeLoan(command[2])
    elif (command[:2] == ["BROWSE", "SHIPS"]):  # BROWSE SHIPS $SYSTEM
        terminal.browseShips(command[2])
    elif (command[:2] == ["BUY", "SHIP"]):  # BUY SHIP $LOCATION $TYPE
        terminal.buyShip(command[2], command[3])
    elif (command[:1] == ["PURCHASE"]):  # PURCHASE $SHIPID $GOODID $QUANTITY
        terminal.purchaseOrder(command[2], command[3], command[4])
    elif (command[:2] == ["BROWSE", "MARKET"]):  # BROWSE MARKET $LOCATION
        terminal.browseMarket(command[2])
    elif (command[:2] == ["SCAN", "SYSTEM"]):  # SCAN SYSTEM $SYSTEM
        terminal.scanSystem(command[2])

    print("Insert your command: (EXIT to shutdown terminal and HELP for help)")
    command = input("").split()
    print("")
# ------------------------------------------------------------------------------------------------
