'''
Date: 4/13/2022

Author: Chance Homme

This script is responsible for using NETCONF to pull a attributes from a device and prints out a detailed report of the retived device data.
The script then will ask the user if they would like to make changes to an interface and will have the user specify the interface, ip address,
subnet mask, and description they would like to put on the interface. The script will change the ordered dictionary that contains the data for
the user specified data and then will print out a report detailing the changes.

'''


# import statements importing various libraries responsible for parsing xml, netconf function and ordered dictionaries

import xml.etree.ElementTree as ET
import xmltodict
import xml.dom.minidom
from lxml import etree
from ncclient import manager
from collections import OrderedDict




def getNETCONF(ipadd): # function responsible for creating the NETCONF API call
    
# lines 30-50 were imported from the turnipTheBeet git repository

    router = {"host": ipadd, "port" : "830",
              "username":"cisco","password":"cisco"}


    netconf_filter = """

    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface></interface>
    </interfaces>
       
    """

    with manager.connect(host=router['host'],port=router['port'],username=router['username'],password=router['password'],hostkey_verify=False) as m:

        netconf_reply = m.get_config(source = 'running', filter = ("subtree",netconf_filter))

    netconf_data = xmltodict.parse(netconf_reply.xml)["rpc-reply"]["data"]

    #Create List of Interfaces

    interfaces = netconf_data["interfaces"]["interface"]

    
    return interfaces



def printReport(response): # function responsible for making a print report of the device info

    print("Interface" +'\t\t' + 'IP' + '\t\t' + 'Subnet' + '\t\t\t' + 'Description') # print statement creating the headers for the report
    print('-' * 100) 
    
    for dictionary in response: # for each of the dictionaries in the response

        inttype = dictionary['type']['#text'] # inttype contains the type attribute of each interface
        
        if inttype == 'ianaift:ethernetCsmacd': # if the interface is not a loopback interface, the function will print the interface name,
                                                # ip address, subnet mask and description of each interface.
            
            print(dictionary['name'] + '\t' + dictionary['ipv4']['address']['ip'] + '\t' + dictionary['ipv4']['address']['netmask'] + '\t\t' + dictionary['description'] )




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
    


def modifyData(apiCall, userSN, userIP, userInt, userDesc): # function responsible for modifying the dicitonary containing the device data


    
    for dictionary in apiCall: # for each of the dictionaries in the apiCall

        intType = dictionary['type']['#text'] # intType contains the type attribute of each interface

        if intType == 'ianaift:ethernetCsmacd': # if the interface is not a loopback interface then a temp variable is specified containing its name
            
            intName = dictionary['name']

            if intName == userInt: # if the interface name is the name of the user desired interface, the ip address, subnet mask, and
                                   # description are changed to the user input changes that were passed to the function

                dictionary['ipv4']['address']['ip'] = userIP

                dictionary['ipv4']['address']['netmask'] = userSN

                dictionary['description'] = userDesc

    return apiCall # the apiCall is returned to main for further use

                




    


############# main code

ipaddress = '10.10.20.175'

apiCall = getNETCONF(ipaddress) # apiCall makes the request to the device to get all device related information

printReport(apiCall) # printReport is called passing the device info stored in apiCall


askUser = userInput('\nWould you like to change attribuites of an interface? [Y or N]: ', ['y','n','Y','N'] )
# the user is asked if they would like to make changes to any interfaces shown

if askUser.lower() == 'n': # if the user doesnt want to make changes, a print statement shows no changes were made
    print('\nNo changes were made to the devices.')


if askUser.lower() == 'y': # if the user does want to make changes, the user will be asked for the interface they would like to change and the
                           # ip address they would like the interface to have

    userInt = input('\nPlease enter the interface name you would like to modify exactly as listed on the device report above: ')

    userIP = input('\nPlease enter the new IP address in x.x.x.x format: ')
    
    validateIP = validIP(userIP) # validateIP calls the validIP function, passing the user specified IP address

        
    while validateIP == False: # if the ip address is not valid the user will be asked to enter a valid ip address

        print('\nThe entered IP address is not a valid IP address.')
        userIP = input('\nPlease enter the new IP address in x.x.x.x format: ')
        validateIP = validIP(userIP)
        
    else:
        userSN = input('\nWhat is the subnet of this IP address? (x.x.x.x format, class A or lower subnets only): ')
        # userSubnet asks the user for the subnet of the above ip address
        
        subnetCheck = validSubnet(userSN) # subnetCheck validates the subnet


        while subnetCheck == False: # if the subnet is deemed not valid, an error statement will print and the user will be prompted 
                                    # again for a subnet address that will be validated again 

            print('\nThe entered subnet is invalid.')

            userSN = input('\nWhat is the subnet of this IP address? (x.x.x.x format, class B or lower subnets only): ')

            subnetCheck = validSubnet(userSN)


        else: 

            userDesc = input('\nPlease enter a description for the interface you would like to modify: ')
            # user is asked to modify the description of the interface 
            
            modifyResponse = modifyData(apiCall, userSN, userIP, userInt, userDesc)
            #modifyResponse calls modifyData, passing the original apiCall data and all the user specified variables to change on the interface

            printReport(modifyResponse)
            # the printReport function is called again using the modified data to print the changes
    












