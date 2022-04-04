'''
Date: 4/4/2022
Author: Chance Homme

This script is responsible for creating a program that retrives interface data from a device, prints the data
and then asks the user if they would like to change an interface. If they want to change the address on an interface, the new interface will be
validated, once determined as valid the old address will be removed and the new one will be added.


'''

import requests # import statements importing request and json libraries
import json

'''

devices = [
    {
        'hostname': 'R1',
        'type':'router',
        'brand':'cisco',
        'mgmtIP':'10.0.0.1'
        },
    {
        'hostname': 'S1',
        'type':'switch',
        'brand':'cisco',
        'mgmtIP':'10.0.0.2'
        },
    ] #  devices is a list of dictionaries containing device information


def createListSubset(listOfDevs):

    newList = []

    for dev in listOfDevs:
        newList.append({'hostname':dev['hostname'], 'mgmtIP':dev['mgmtIP']})

    return newList




print(devices)

modList = createListSubset(devices)

print(modList)

for device in modList:
    print(device)


'''





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
    # repsone sends the api post call to the location specified in the url variable

#    print(response.json())
    
    return response.json() # the response is returned in json to main for further use



def getIntfRestMAC(mgmtIP):
    
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
    # repsone sends the api post call to the location specified in the url variable

#    print(response.json())
    
    return response.json() # the response is returned in json to main for further use



def combineIntLists(rawintfList,rawintfStateList):
    

    intfList = rawintfList['ietf-interfaces:interfaces']['interface']

    intfStateList = rawintfStateList['ietf-interfaces:interfaces-state']['interface']
    
    tempList = []

    combinedList = []
    
    for interface in intfList:

        if interface['type'] == 'iana-if-type:ethernetCsmacd':

            combinedList.append({'Name':interface['name'], 'IP':interface['ietf-ip:ipv4']['address'][0]['ip']})

    for interface in intfStateList:

        if interface['type'] == 'iana-if-type:ethernetCsmacd':

            tempList.append({'MAC':interface['phys-address']})

    count = 0
        
    for dictionary in combinedList:

        dictionary.update(tempList[count])

        count += 1    
    
    return combinedList

    


def printList(masterList):

    # print statements setting up the formatting for the list of interfaces

    print('\n' + 'Interface Name\t\t' + 'IP Address\t\t' + 'MAC\t\t')
    print('\n' + "-" * 100)


    for item in masterList: # for each of the dictionaries in the masterList, print the values of Name, IP, and MAC to match the headers.

        print('\n',item['Name'],'\t',item['IP'],'\t\t',item['MAC'],'\t\t')


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


def validCIDR(CIDR):

    validCIDR = True

    if CIDR.isalpha() == True:

        validCIDR = False
        return validCIDR
    
    if CIDR.isnumeric() == False:
        
        validCIDR = False

    if int(CIDR) < 1 or int(CIDR) >= 32:

        validCIDR = False

    return validCIDR     
    

### Main code

ipAddr = '10.10.20.175'

intList =  getIntfRest(ipAddr)

intStateList = getIntfRestMAC(ipAddr)

combinedIntList = combineIntLists(intList, intStateList)

printList(combinedIntList)

askUser = userInput('Would you like to change an IP address on an interface? [Y or N]: ', ['y','n','Y','N'])

if askUser.lower() == 'n':
    print('No interface addresses were changed at this time.')

if askUser.lower() == 'y':

    userIP = input('Please enter the new IP address in x.x.x.x format: ')
    validateIP = validIP(userIP)

        
    while validateIP == False: # if the ip address is not valid the user will be asked to enter a valid ip address

        print('The entered IP address is not a valid IP address.')
        userIP = input('Please enter the new IP address in x.x.x.x format: ')
        validateIP = validIP(userIP)
        
    else:
        userCIDR = input('Please enter the length of the subnet mask for this address (ex 24 = /24 = 255.255.255.0): ')

        validateCIDR = validCIDR(userCIDR)

        while validateCIDR == False:
            
            print('The entered subnet mask length is not valid.')
            userCIDR = input('Please enter the length of the subnet mask for this address (ex 24 = /24 = 255.255.255.0): ')
            validateCIDR = validCIDR(userCIDR)

        else:
            print('valid')











