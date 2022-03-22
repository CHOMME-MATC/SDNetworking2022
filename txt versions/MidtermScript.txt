'''
Author: Chance Homme
Date: 3/8/22

This script is responisble for changing the ip addresses on all vlan interfaces by 5 on the last octet
on any given switch based on it's management ip address.
The script will ask for the management ip address and display the current vlan interfaces and their ip addresses as well as
the vlan interfaces with the changed addresses once they have been changed.

'''


import requests # command importing the requests library
import json # command importing the json library


def userInput(prompt, answerList): #User input function

    answer = input(prompt) #variable that tracks the users input according to the prompt that was passed to the function.

    while answer not in answerList: #while loop that will return the initial inpuy prompt if the users answer is not valid 
        print('Please respond using a valid answer.')
        answer = input(prompt)
    
    return answer #The answer will be returned once a valid answer is entered.


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

    count = 0 # count is stand-in variable used to represent the current list item being iterated through in apiResponse

    for interface in apiResponse: # for loop is declaring the key of apiResponse[count]['intf-name'] as a temp variable,
                              #if the variable starts with V indicating a vlan interface, the attributes of the vlan interface are stored as temp variables,
                              # they are then checked for length requirements, if they are less than or equal to 8 characters, they will need to add
                              # a tab to line up to the column headers, once the if statements are cleared, the print statement will print each variable
                              # whilst adding a tab to space out the variables and increment the count and repeat the process until all vlan interfaces
                              # from the list of dictionaries from the apiResponse are printed.

        
        intName = apiResponse[count]['intf-name']

        if intName.startswith('V') == True:

            vlanInt =  apiResponse[count]['intf-name']   
            intProto = apiResponse[count]['proto-state']
            intLink = apiResponse[count]['link-state']
            intPfix = apiResponse[count]['prefix']
            
            if len(intName) <= 8 and intName.startswith('V') == True: 
                intName = apiResponse[count]['intf-name'] + '\t'


            if len(intProto) <= 8:
                intProto = apiResponse[count]['proto-state'] + '\t'

            if len(intLink) <= 8:
              intLink = apiResponse[count]['link-state']  + '\t'

            print( vlanInt, '\t', intProto, '\t', intLink, '\t', intPfix)
            count += 1



def apiToDict(apiResponse): #Function responsible for turning the api call of interfaces into a dictionary of just VLAN interfaces with attributes

        intfDict = {} # apiDict is an empty dictionary which will hold information for all vlan interfaces
        
        count = 0 # count is stand-in variable used to represent the current list item being iterated through in apiResponse

        for interface in apiResponse: 

            intName = apiResponse[count]['intf-name']

            if intName.startswith('V') == True:

                vlanInt =  apiResponse[count]['intf-name']   
                intAdd = apiResponse[count]['prefix']
                intfDict[vlanInt] = {}
                intfDict[vlanInt]['Name'] = vlanInt
                intfDict[vlanInt]['IP'] = intAdd
                count += 1
        
        return intfDict # intfDict is returned to main for further use
                
            
def addIPValue(ip): # Function responsible for creating the new ip address

    seperateOctets = ip.split('.') #variable that splits the ip on the decimals for easier handling of octets
    
    octetList = [] #empty list which will contain octets       

    for octet in seperateOctets: #for loop adding all octets of the ip address to the list of octets
        octetList.append(octet)

    octetList[3] = int(octetList[3]) + 5 # The last octet of the address will be changed to an integer and have 5 added to it, after that
                                         # has been done, it will be turned back into a string and concatenated with the other octets in
                                         # octetList to be stored as one string value which is will be stored as the ipPlusFive variable

    octetList[3] = str(octetList[3])

    ipPlusFive = octetList[0]+'.'+octetList[1]+'.'+octetList[2]+'.'+octetList[3]

    return ipPlusFive # ipPlusFive is returned for further use



def addIP(devip, interface, newip): # function responsible for creating the api call that pushes the ip address change
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
          "cmd": "ip address " + newip + " 255.255.255.0",
          "version": 1
        },
        "id": 3
      }
    ]

    
    response = requests.post(url,data=json.dumps(payload), verify=False, headers=myheaders,auth=(switchuser,switchpassword)).json()

    # response was edited to include verify = False to circumvent the default certification validation





################################################### main code


devices = {   # dictionary containing all known dist switches on the network
    'dist-sw01': '10.10.20.177',
    'dist-sw02': '10.10.20.178'
    }



# this print statement explains the function of the code before executing
print('''
===================================================================================================================================================
This program was created in response to the recent upgrade which will increase fault tollerance to the network.
The current objective of this program is designed to scan any given NXOS capable switch and display the current VLAN interfaces,
when prompted, you may choose to increase the addressing on all VLAN interfaces by 5 on the last octet of the address displayed for the interfaces.
Otherwise you may opt out of change and the program will end stating no changes were made.

A preconfigured list of devices will be shown, otherwise you may choose to enter a valid IP address of your choosing to have changes made to.
===================================================================================================================================================
\n
''')


# print statements are displaying the current devices on the network
print('The current known devices on this network are:  \n')

print(' Device Name \t\t Management IP')

print('\n' + "-" * 50)

for key in devices:
    print( key + '\t\t' + devices[key])


#askForMass is used to store the user input of wether they wouldn like to change all known devices or not
askForMass = userInput('\nWould you like to push changes to all known devices?[Y or N]: ', ['y','n','Y','N'])


if askForMass.lower() == 'y': # if the user wants to change the known devcies, the management ip of the devices listed in the devices dictionary are
                              # are used to create api calls and show all vlan interfaces currently on each device, a message pops up asking the
                              # user if they are sure if they would like to change the ip addresses on the shown vlan interfaces

    print('\nThe following interfaces are selected to have address changes pushed:  \n') 

    knownDevices = [] # knownDevices is an empty dictionary 
    
    for address in devices:
        
        importedMGMT = devices[address]
        
        shMassIntCMD = sendToCLI(importedMGMT, 'sh ip int br')

        printMassInt = showInterfaces(shMassIntCMD)        

        knownDevices.append(importedMGMT)
        
    
    askForMassChange = userInput('\nAre you sure you want to make address changes to the VLAN interfaces on this switch? [Y or N]: ', ['Y','N','y','n'])


    if askForMassChange.lower() == 'n': # if the user doesnt want to change the addresses, a print statement shows there was no changes made

        print('\nNo changes were made to known devices.')



    if askForMassChange.lower() == 'y': # if the user confirms the change the following will occur

        for managementIP in knownDevices: # for each of the mgmt ip's in knownDevices, a sh ip int br api call is made and sent to the apiToDict
                                          # function where the whole output is refined to just vlan interfaces and returned as a dictionary

            shIntCMD = sendToCLI(managementIP, 'sh ip int br')
                
            vlanDict = apiToDict(shIntCMD)

            for interface in vlanDict: # for each interface contained in the dictionary, the nested dictonary value containing the ip address of
                                       # the interface is declared as oldAddress, then oldAddress is passed through addIPValue to add 5 to the
                                       # last octet of the ip address and is stored as newIP. newIP is used to overwrite the old IP address in
                                       # the vlanDict and an address change is made to the interface using the addIP function.
              
                oldAddress = vlanDict[interface]['IP']
              
                newIP = addIPValue(oldAddress)
              
                vlanDict[interface]['IP'] = newIP

                addressChange = addIP(managementIP, interface, newIP)


        for managementIP in knownDevices:

            shIPNew = sendToCLI(managementIP, 'sh ip int br') # new api calls are made to display the current ip addresses of the changed vlan
                                                              # interfaces, then a print statement shows that the vlan interfaces were changed.
          
            printIPNew = showInterfaces(shIPNew)

            print('The VLAN interface addresses on this device were successfully changed.')
          

                
                
        

if askForMass.lower() == 'n': # if the user doesnt want to push the changes to all known devices, they still have an option to choose a single
                              # device to change
    
    askForMGMT = input('\nEnter the Management IP address of the switch you would like to configure: ') # askForMGMT stores user specified mgmt ip address

    validateIP = validIP(askForMGMT) # the address is validated via the valid ip function


    while validateIP == False: # if the ip address is not valid the user will be asked to enter a valid ip address
          
          print('The entered IP address is not a valid IP address.')
          askForMGMT = input('Enter the Management IP address of the switch you would like to configure: ')

    else: # if the ip address is valid, the user specified ip address is stored as validMGMT and is passed through api calls that
          # show the vlan interfaces and addresses on the specified device  
        validMGMT = askForMGMT
        
        print('The following interfaces are selected to have address changes pushed:  \n')

        shIntCMD = sendToCLI(validMGMT, 'sh ip int br')

        printInt = showInterfaces(shIntCMD)

        askForChange = userInput('Are you sure you want to make address changes to the VLAN interfaces on this switch? [Y or N]: ', ['Y','N','y','n'])
        # the user is asked if they are sure they want to change the ip address of all the vlan interfaces on this device


    if askForChange.lower() == 'n': # if the user doesnt want to change the addresses, a print statement shows there was no changes made
          print('No Changes were made to the specified switch.')



    if askForChange.lower() == 'y': # if the user confirms they would like to change the ip addreses for the device the following will occur

          vlanDict = apiToDict(shIntCMD) # the response from the inital api call for show ip int br is passed through apiToDict to convert the
                                         # call into a dictionary with only vlan interfaces and params of vlan interfaces

          for interface in vlanDict: # for each of the vlan interfaces stored in vlanDict, the nested dictonary value containing the ip address of
                                     # the interface is declared as oldAddress, then oldAddress is passed through addIPValue to add 5 to the
                                     # last octet of the ip address and is stored as newIP. newIP is used to overwrite the old IP address in
                                     # the vlanDict and an address change is made to the interface using the addIP function.

              
              oldAddress = vlanDict[interface]['IP']
              
              newIP = addIPValue(oldAddress)
              
              vlanDict[interface]['IP'] = newIP

              addressChange = addIP(validMGMT, interface, newIP)

          shIPNew = sendToCLI(validMGMT, 'sh ip int br')
          
          printIPNew = showInterfaces(shIPNew) # new api calls are made to display the current ip addresses of the changed vlan
                                               # interfaces, then a print statement shows that the vlan interfaces were changed.
                                               
          print('The VLAN interface addresses on this device were successfully changed.')
          
         
      



