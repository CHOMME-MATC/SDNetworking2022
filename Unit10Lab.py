'''
Date: 4/4/2022
Author: Chance Homme

This script is responsible for creating a program that retrives interface data from a device, prints the data
and then asks the user if they would like to change an interface. If they want to change the address on an interface, the new interface will be
validated, once determined as valid the old address will be removed and the new one will be added.


'''

import requests # import statements importing request, time, and json libraries
import json
import time



def getIntfRest(mgmtIP): # function responsible for retriveing the nested dictionary containing info on the devices interfaces 

# lines 19-31 are imported from the turnipTheBeet GIT repository with some alterations to the url variable to pass mgmtIP

    url = "https://"+ mgmtIP +"/restconf/data/ietf-interfaces:interfaces" # url contains the destination for the api call, with mgmtIP 
                                                                          # being the ip address of the device being passed to the function

    username = 'cisco' # username and password contain the username and password to authenticate with the device
    password = 'cisco'
    payload={} # payload is empty to retrive all data from the url location
    headers = { # headers specify the type of data being requested, and the authorization type
      'Content-Type': 'application/yang-data+json',
      'Accept': 'application/yang-data+json',
      'Authorization': 'Basic cm9vdDpEX1ZheSFfMTAm'
    }

    response = requests.request("GET", url, auth = (username,password), verify = False, headers=headers, data=json.dumps(payload))
    # repsone sends the api get call to the location specified in the url variable

    
    return response.json() # the response is returned in json to main for further use



def getIntfRestMAC(mgmtIP): # function responsible for retriveing the nested dictionary containing info on the interface statuses 
    
    # lines 19-31 are imported from the turnipTheBeet GIT repository with some alterations to the url variable to pass mgmtIP

    url = "https://"+ mgmtIP +":443/restconf/data/interfaces-state" # url contains the destination for the api call, with mgmtIP 
                                                                          # being the ip address of the device being passed to the function

    username = 'cisco' # username and password contain the username and password to authenticate with the device
    password = 'cisco'
    payload={} # payload is empty to retrive all data from the url location
    headers = { # headers specify the type of data being requested, and the authorization type
      'Content-Type': 'application/yang-data+json',
      'Accept': 'application/yang-data+json',
      'Authorization': 'Basic cm9vdDpEX1ZheSFfMTAm'
    }

    response = requests.request("GET", url, auth = (username,password), verify = False, headers=headers, data=json.dumps(payload))
    # repsone sends the api get call to the location specified in the url variable


    return response.json() # the response is returned in json to main for further use



def combineIntLists(rawintfList,rawintfStateList): # function combining both lists containing the interface status and the interface information
    

    intfList = rawintfList['ietf-interfaces:interfaces']['interface'] # intfList parses the raw response from getIntfRest to the list of dicitonaries

    intfStateList = rawintfStateList['ietf-interfaces:interfaces-state']['interface']
    # intfStateList parses the raw response from getIntfRestMAC to the list of dicitonaries
    
    tempList = [] # tempList is an empty list designed to keep intfStateList contents in

    combinedList = [] # combinedList is an empty list designed to keep both list contents in
    
    for interface in intfList: # for each of the dictionaries in intfList, if the type value is listed as iana-if-type:ethernetCsmacd,
                               # the interface names and ip addresses are appended as a dictionary to combinedList

        if interface['type'] == 'iana-if-type:ethernetCsmacd':

            combinedList.append({'Name':interface['name'], 'IP':interface['ietf-ip:ipv4']['address'][0]['ip']})

    for interface in intfStateList: # for each of the dictionaries in intfStateList, if the type value is listed as iana-if-type:ethernetCsmacd,
                                    # the interface mac addresses are appended as a dictionary to tempList
                                    
        if interface['type'] == 'iana-if-type:ethernetCsmacd':

            tempList.append({'MAC':interface['phys-address']})

    count = 0 # count is used to iterate through the items in tempList
        
    for dictionary in combinedList: # for each of the nested dictionaries contained in combinedList, the dictionary needs to be appended with
                                    # the corrosponding item in tempList to complete the list of dictionaries. count is incremented by one to
                                    # iterate through the tempList

        dictionary.update(tempList[count])

        count += 1
    
    return combinedList # the list is returned to main for further use

    


def printList(masterList):

    # print statements setting up the formatting for the list of interfaces

    print('\n' + 'Interface Name\t\t' + 'IP Address\t\t' + 'MAC')
    print('\n' + "-" * 100)


    for item in masterList:
# for each of the dictionaries in the masterList, print the values of Name, IP, and MAC to match the headers. If the IP value is more than 
# 13 characters it will need one less tab to properly allign the formatting with the headers.

        if len(item['IP']) <= 13:
            
            print('\n',item['Name'],'\t',item['IP'],'\t\t',item['MAC'])

        else:
           print('\n',item['Name'],'\t',item['IP'],'\t',item['MAC']) 



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
    


def changeAddress(mgmtIP,userIP,userMask,userInterface): # function used to push the ip address change to the users parameters on the device
# lines 197-222 are imported from the turnipTheBeet GIT repository with some alterations to the url and payload variables to pass mgmtIP,
# userIP,userMask, and userInterface to the API call.

    time.sleep(60) # time is used to delay the program by 60 seconds in order to allow for manual removal of the interface address
    
    url = "https://" + mgmtIP + ":443/restconf/data/ietf-interfaces:interfaces/interface=" + userInterface
# url contains the destination for the api call, with mgmtIPbeing the ip address of the device being passed to the function and userInterface
# specifying the interface as the parameter in the url     

    
    username = 'cisco' # username and password contain the username and password to authenticate with the device
    password = 'cisco'
    payload={"ietf-interfaces:interface": { # payload iterates through the YANG model using the userInterface variable to specify the interface
                    "name": userInterface, # userIP as the new address and userMask as the new subnet mask
                    "description": "Configured by RESTCONF",
                    "type": "iana-if-type:ethernetCsmacd",
                    "enabled": "true",
                                     "ietf-ip:ipv4": {
                                                            "address": [{
                                                                "ip": userIP,
                                                                "netmask": userMask
                                                                }]}}}


    headers = { # headers specify the type of data being requested, and the authorization type
    'Authorization': 'Basic cm9vdDpEX1ZheSFfMTAm',
    'Accept': 'application/yang-data+json',
    'Content-Type': 'application/yang-data+json'
    }

    response = requests.request("PUT", url, auth=(username,password),headers=headers, verify = False, data=json.dumps(payload))
    # repsone sends the api put call to the location specified in the url variable





### Main code

ipAddr = '10.10.20.175' # ipAddr contains the address of dist-rtr01 

intList =  getIntfRest(ipAddr) # intList calls the getIntfRest function passing ipAddr to the function

intStateList = getIntfRestMAC(ipAddr) # intStateList calls the getIntfRestMAC function passing ipAddr to the function

combinedIntList = combineIntLists(intList, intStateList) # combinedIntList calls the combineIntLists function passing intList and intStateList to the function

printList(combinedIntList) # printList is called, passing combinedIntList to the function

askUser = userInput('\nWould you like to change an IP address on an interface? [Y or N]: ', ['y','n','Y','N']) # askUser calls the userInput
                                                                # function to ask if they would like to change an ip address on an interface

if askUser.lower() == 'n': # if the user declines, a print statement saying nothing has been changed will display
    print('\nNo interface addresses were changed at this time.')

if askUser.lower() == 'y': # if the user wants to change an interface address, they will be asked for the name of the interface and the
                           # ip address of the interface. The ip will be checked for validity using validIP

    userInterface = input('\nPlease enter the name of the interface you would like to change exactly as displayed on the above report: ')
    userIP = input('\nPlease enter the new IP address in x.x.x.x format: ')
    validateIP = validIP(userIP)

        
    while validateIP == False: # if the ip address is not valid the user will be asked to enter a valid ip address

        print('\nThe entered IP address is not a valid IP address.')
        userIP = input('\nPlease enter the new IP address in x.x.x.x format: ')
        validateIP = validIP(userIP)
        
    else:
        userSubnet = input('\nWhat is the subnet of this IP address? (x.x.x.x format, class A or lower subnets only): ')
        # userSubnet asks the user for the subnet of the above ip address
        
        subnetCheck = validSubnet(userSubnet) # subnetCheck validates the subnet


        while subnetCheck == False: # if the subnet is deemed not valid, an error statement will print and the user will be prompted 
                                    # again for a subnet address that will be validated again 

            print('\nThe entered subnet is invalid.')

            userSubnet = input('\nWhat is the subnet of this IP address? (x.x.x.x format, class B or lower subnets only): ')

            subnetCheck = validSubnet(userSubnet)


        else: 
            print('\nManually clear out the IP address of this interface, you have 60 seconds to do so before the code automatically executes.')
            
            updateDevice = changeAddress(ipAddr,userIP,userSubnet,userInterface)

            intList =  getIntfRest(ipAddr)

            intStateList = getIntfRestMAC(ipAddr)

            combinedIntList = combineIntLists(intList, intStateList)

            printList(combinedIntList)


'''
Once both the subnet and the ip are validated, a message states that the user must manually clear the address from the device to prevent
secondary addresses from accumulating on the interface. Once 60 seconds has passed, the changeAddress function passes pAddr,userIP,userSubnet,
and userInterface to make the specified changes to the device, and the intList, intStateList, combinedIntList and printList functions are
re-ran to collect the correct information about the devices and reprint the report showing the newly modified address on the interface
'''












