'''
Date: 3/1/2022
Author: Chance Homme

This script is responsible for allowing users to change the ip address of any given interface on dist-sw01 class A subnets or lower.

'''


import requests # command importing the requests library
import json # command importing the json library

"""
Be sure to run feature nxapi first on Nexus Switch

"""

def sendToCLI(ipaddress, command): # function responsible for sending general commands to cli

    switchuser='cisco' # variable containing the username for the switch login
    switchpassword='cisco' # variable containing the password for the switch login

    url='https://' + ipaddress + '/ins' # variable containing the destination of the api call
    myheaders={'content-type':'application/json-rpc'} 
    payload=[
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "config t",
          "version": 1
        },
        "id": 1
      },
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": command,
          "version": 1
        },
        "id": 2
      }
    ]

    # variable containing responsible for containing api call, verify=False is added to circumvent certification validation
    response = requests.post(url,data=json.dumps(payload), verify=False,headers=myheaders,auth=(switchuser,switchpassword)).json() 
    
    intDict = response[1]['result']['body']['TABLE_intf']['ROW_intf'] # variable narrowing down the usable part of the api call containing 
                                                                      # the list of dictionaries containing interface attributes
                                                                      
    return intDict # response dictionary is returned to main for further use



def showInterfaces(apiResponse): # function responsable for creating the show ip interface report statement 
                                                          
    # print statements setting up the formatting for the list of interfaces
    print('\n' + 'Name\t\t' + 'Proto\t\t' + 'Link\t\t' + 'Address\t\t')
    print('\n' + "-" * 135)

    count = 0 # count is stand-in variable used to represent the current list item being iterated through in intDict

    for interface in apiResponse: # for loop is declaring the keys of apiResponse[count] as seperate variables, once they are put into the temp variables,
                              # they are then checked for length requirements, if they are less than or equal to 8 characters, they will need to add
                              # a tab to line up to the column headers, once the if statements are cleared, the print statement will print each variable
                              # whilst adding a tab to space out the variables and increment the count and repeat the process until the list of dictionaries
                              # has been fully iterated through.
                              
        intName = apiResponse[count]['intf-name']
        intProto = apiResponse[count]['proto-state']
        intLink = apiResponse[count]['link-state']
        intPfix = apiResponse[count]['prefix']
        
        if len(intName) <= 8: 
            intName = apiResponse[count]['intf-name'] + '\t'

        if len(intProto) <= 8:
            intProto = apiResponse[count]['proto-state'] + '\t'

        if len(intLink) <= 8:
          intLink = apiResponse[count]['link-state']  + '\t'

        print( intName, '\t', intProto, '\t', intLink, '\t', intPfix)
        count += 1


def userInput(prompt, answerList): #User input function

    answer = input(prompt) #variable that tracks the users input according to the prompt that was passed to the function.

    while answer not in answerList: #while loop that will return the initial inpuy prompt if the users answer is not valid 
        print('Please respond using a valid answer.')
        answer = input(prompt)
    
    return answer #The answer will be returned once a valid answer is entered.


def validInt(apiCall): # function creating a list of valid interfaces stored on the switch 

    intList = [] # intList is an empty list used to store the interface names
    
    for item in apiCall: # for each item in the list of dictionaries, interface is specified as the value of item['intf-name'],
                         # formattedInt then normalized the response to all lowercase and appends each entry to the intList
        
        interface = item['intf-name']

        formattedInt = interface.lower()

        intList.append(formattedInt)

    return intList # intList is returned for further use


def validIP(IP): #Function validating user input ip
    
    validIP = True #Flag measuring if the ip is valid or not

    if IP.count('.') != 3: #if loop measuing the ammount of decimals in the ip for proper formatting
        validIP = False

    ipCheck = IP.split('.') #variable that splits the ip on the decimals for easier handling of octets
    
    octetList = [] #empty list which will contain octets
    
    if len(ipCheck) !=4: #if loop stating that if the ammount of octets is not equal to four, the valid flag will be set false
        validIP = False
    
    for octet in ipCheck: #for loop iterating through all items in ipCheck
        octetList.append(octet)
        if octet.isnumeric() == False: #if statement checking if the octet string is strictly numeric
            validIP = False
            return validIP
        if int(octet) < 0 or int(octet) > 255: # if statement verifying that the octets are in the valid range for ipv4 addresses
            validIP = False
        if int(octetList[0]) == 0: # if statement ensuring that the first octet is not equal to zero
            validIP = False
        
    return validIP # validIP returned to main for further use


def validSubnet(SN): #Function validating user input subnet
    
    validSN = True #Flag measuring if the subnet is valid or not

    if SN.count('.') != 3: #if loop measuing the ammount of decimals in the subnet for proper formatting
        validSN = False

    snCheck = SN.split('.') #variable that splits the subnet on the decimals for easier handling of octets
    
    subnetList = [] #empty list which will contain octets of subnet
    
    if len(snCheck) !=4: #if loop stating that if the ammount of octets is not equal to four, the valid flag will be set false
        validSN = False
    
    for octet in snCheck: #for loop iterating through all items in snCheck
        subnetList.append(octet)
        if octet.isnumeric() == False: #if statement checking if the octet string is strictly numeric
            validSN = False
            return validSN
        if int(octet) < 0 or int(octet) > 255: # if statement verifying that the octets are in the valid range for subnet addresses
            validSN = False

    if int(subnetList[0]) != 255: # if statement ensuring that the first octet is equal to 255

        validSN = False
        
    if int(subnetList[1]) < 255 and int(subnetList[2]) != 0: # if statement stating that if the second octet is less than 255, the subsequent 
                                                             # octet must be 0 to be valid
        validSN = False

    if int(subnetList[2]) < 255 and int(subnetList[3]) != 0: # if statement stating that if the third octet is less than 255, the subsequent 
                                                             # octet must be 0 to be valid
        validSN = False
        
    return validSN # validIP returned to main for further use       
    

def addIP(devip, interface, newip, newsn): # function responsible for creating the api call that pushes the ip address change
                                           # devip is passed for the url ip, interface is used to specify the interface that will need a new
                                           # ip address, newip and newsn are passed as the user specified ip address and subnet that will be used

    switchuser='cisco' # switchuser contains the string value of the username for the switch user account
    switchpassword='cisco' # switchpassword contains the string value of the password for the switch user account

    url='https://' + devip + '/ins' # variable containing the destination of the api call
    myheaders={'content-type':'application/json-rpc'} # my headers, payload, and response were auto generated by the NEXOS api to create an API call
                                                      # that issues the conf t, interface, and ip address commands on the switch using the destination url,
                                                      # interface was added to specify the interface for the interface command, as well as the newip
                                                      # and newsn commands for the ip address command syntax
    
    payload=[
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "conf t ",
          "version": 1
        },
        "id": 1
      },
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "interface " + interface,
          "version": 1
        },
        "id": 2
      },
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "ip address " + newip + " " + newsn,
          "version": 1
        },
        "id": 3
      }
    ]

    
    response = requests.post(url,data=json.dumps(payload), verify=False, headers=myheaders,auth=(switchuser,switchpassword)).json()

    # response was edited to include verify = False to circumvent the default certification validation



#main code

DS1 = '10.10.20.177' # variable containing Distribution switch 1's ip address

cliCall = sendToCLI(DS1, 'show ip interface brief') # variable containing the function creating the api call for the show ip int br command

intReport = showInterfaces(cliCall) # intReport calls the showInterfaces function and passes the show ip int brief raw api response to be formatted

listOfInt = validInt(cliCall) # listOfInt calls the validInt to create a list of all interfaces captured from the inital sh ip int br command

print('\nThe device selected for configuration is dist-sw01') # print statement showing the user which device they are configuring

askUser = userInput('\nWould you like to change any IP addresses? [Y or N]: ', ['y','Y','n','N']) # askUser calls the userInput function to ask if
                                                                                                  # they want to make a change to any ip addresses

if askUser.lower() == 'y': # if the user response is y, they following will occur

    desiredInt = input('Which interface would you like to configure? ') # desiredInt contains the user specified interface they would like to change

    while desiredInt.lower() not in listOfInt: # if the normalized user response is not a valid interface, an error print statement will say it
                                               # doesnt exist on the device and it will loop back to the original input statement

        print('That interface does not exist on this device')

        desiredInt = input('Which interface would you like to configure? ')

    if desiredInt.lower() in listOfInt: # if the interface name is valid, userInt will contain the interface name in proper capitalization

        userInt = desiredInt.capitalize()
        
        userIP = input('\nWhat address would you like to change the interface to? (x.x.x.x format): ') # userIP asks the user for the new ip address

        ipCheck = validIP(userIP) # ipCheck validates the user specified IP

        while ipCheck == False: # if the ip address is not valid, an error statement will print and the user will be prompted 
                                # again for an ip address that will be validated again
                                
            print('The entered IP is invalid')

            userIP = input('\nWhat address would you like to change the interface to? (x.x.x.x format): ')

            ipCheck = validIP(userIP) 
            

        userSubnet = input('\nWhat is the subnet of this IP address? (x.x.x.x format, class A or lower subnets only): ') # user subnet asks the user 
                                                                                                                         # for the subnet of the above ip address
        subnetCheck = validSubnet(userSubnet) # subnetCheck validates the subnet


        while subnetCheck == False: # if the subnet is deemed not valid, an error statement will print and the user will be prompted 
                                    # again for a subnet address that will be validated again 

            print('The entered subnet is invalid.')

            userSubnet = input('\nWhat is the subnet of this IP address? (x.x.x.x format, class B or lower subnets only): ')

            subnetCheck = validSubnet(userSubnet)
        
        
        if subnetCheck == True and ipCheck == True: # if both the IP and the subnet are valid the following will occur
            
            changeIP = addIP(DS1, userInt, userIP, userSubnet) # changeIP calls the addIP function and passes to it the address of dist-sw01,
                                                               # and the user specified interface, ip address and subnet mask to create the change

            newCLICall = sendToCLI(DS1, 'show ip interface brief') # newCLICall makes a new api call for the show ip interface brief command

            intReport = showInterfaces(newCLICall) # intReport creates a new formatted report of the show ip int brief command with the updated address

            print('\nThe ' + userInt + ' interface has a new IP address of ' + userIP + ' and a subnet mask of ' + userSubnet+'.')
                                                                                                            
            # a print statement details which interface the user has configured, and what ip address and subnet mask it now is configured with

    
if askUser.lower() == 'n': # if the user doesnt want to change the ip address, a print statement will show no changes were made

    print('No IP address changes were configured.')
    



