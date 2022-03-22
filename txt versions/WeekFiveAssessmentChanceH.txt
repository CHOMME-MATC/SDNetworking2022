'''
Date: 2/16/2021
Author: Chance Homme

This code is responsible for issuing a 'show ip interface brief' command to dist-switch-1 via the NEXOS API
and displaying the output of the command in a formatted print statement showing the interface name, the ip address, and the interface status.

'''

import requests # command importing the requests library
import json # command importing the json library

"""
Be sure to run feature nxapi first on Nexus Switch

"""

def sendToCLI(ipaddress, command): # function responsible for sending commands to cli

    switchuser='cisco' # variable containing the username for the switch login
    switchpassword='cisco' # variable containing the password for the switch login

    url='https://' + ipaddress + '/ins' # variable containing the destination of the 
    myheaders={'content-type':'application/json-rpc'} # variable containing 
    payload=[ 
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": command,
          "version": 1
        },
        "id": 1
      }
    ]

    # variable containing responsible for containing api call
    response = requests.post(url,data=json.dumps(payload), verify=False,headers=myheaders,auth=(switchuser,switchpassword)).json() 

    return(response) # response dictionary is returned to main for further use

'''

verify=False below is to accept untrusted certificate

'''


#main code

DS1 = '10.10.20.177' # variable containing Distribution switch 1's ip address

cliCall = sendToCLI(DS1, 'show ip interface brief') # variable containing the function creating the api call

intDict = cliCall['result']['body']['TABLE_intf']['ROW_intf'] # variable narrowing down the usable part of the api call containing 
                                                              # the list of dictionaries containing interface attributes
                                                              
# print statements setting up the formatting for the list of interfaces
print('\n' + 'Name\t\t' + 'Proto\t\t' + 'Link\t\t' + 'Address\t\t')
print('\n' + "-" * 135)

count = 0 # count is stand-in variable used to represent the current list item being iterated through in intDict

for interface in intDict: # for loop is declaring the keys of intDict[count] as seperate variables, once they are put into the temp variables,
                          # they are then checked for length requirements, if they are less than or equal to 8 characters, they will need to add
                          # a tab to line up to the column headers, once the if statements are cleared, the print statement will print each variable
                          # whilst adding a tab to space out the variables and increment the count and repeat the process until the list of dictionaries
                          # has been fully iterated through.
                          
    intName = intDict[count]['intf-name']
    intProto = intDict[count]['proto-state']
    intLink = intDict[count]['link-state']
    intPfix = intDict[count]['prefix']
    
    if len(intName) <= 8: 
        intName = intDict[count]['intf-name'] + '\t'

    if len(intProto) <= 8:
        intProto = intDict[count]['proto-state'] + '\t'

    if len(intLink) <= 8:
      intLink = intDict[count]['link-state']  + '\t'

    print( intName, '\t', intProto, '\t', intLink, '\t', intPfix)
    count += 1


