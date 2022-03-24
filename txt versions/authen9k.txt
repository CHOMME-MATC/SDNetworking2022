'''
Date: 3/23/22
Author: Chance Homme

This script is responsible for exploring RESTful DME models and creating programs utilizing
RESTful DME models in programs used to push device changes.

'''



import requests # import statements importing request and json libraries
import json



#getCookie was imported from the turnipTheBeet git repository

def getCookie(addr): # function responsible for renewing the authentication cookie


    url = "https://"+ addr + "/api/aaaLogin.json" # url contains the destination for the api call, with addr being the passed ip address of the
                                                  # device being passed to the function
 
    payload= {"aaaUser" : # the payload contains the username and password to authenticate with the nxos api 
              {"attributes" :
                   {"name" : "cisco",
                    "pwd" : "cisco"}
               }
          }

    response = requests.post(url, json=payload, verify = False) # repsone sends the api call to the location specified in the url variable

    return response.json()["imdata"][0]["aaaLogin"]["attributes"]["token"] # the api response is returned to the program for further use 



#Get Session Cookie for NX switch. Change address below as needed

address = '10.10.20.177' # address stores the ip address for dist-sw01

#Use the cookie below to pass in request. Cookie is good for 600 seconds

cookie = getCookie(address) # cookie calls the getCookie function passing the address variable to get the authentication token from the device 




### Question 17

url = "https://10.10.20.177/api/mo/sys.json" # url contains the destination for the dme model system for dist-sw01

payload={ # payload iterates through from the top system all the way down to the vlan101 interface and writes a new ip address under the 
"topSystem": { # addr attribute
"children": [
{
"ipv4Entity": {
"children": [
{
"ipv4Inst": {
"children": [
{
"ipv4Dom": {
"attributes": {
"name": "default"
},
"children": [
{
"ipv4If": {
"attributes": {
"id": "vlan101"
},
"children": [
{
"ipv4Addr": {
"attributes": {
"addr": "172.16.151.10/24"
}}}]}}]}}]}}]}}]}}



headers = { # headers specify the type of input sent to the api and the cookie that is being used to authenticate with the device
  'Content-Type': 'text/plain',
  'Cookie': 'APIC-cookie=' + cookie
}

response = requests.request("POST", url, verify=False, headers=headers, data=json.dumps(payload)) # repsone sends the api post call to the location specified in the url variable

print(response.text) # the response is printed from the call ensuring a 200 code is sent back ensuring the call was valid





### Question 27


url = "https://10.10.20.177/api/node/mo/sys/ipv4/inst/dom-default/if-[vlan101].json?query-target=children" #  url contains the destination for
                    # dist-sw01's vlan101 interface child attributes 

payload={ # payload is specifying the new address for the addr attribute under vlan101 
"ipv4Addr": {
"attributes": {
"addr": "172.16.151.10/24",
"type": "primary"
}}}

headers = { # headers specify the type of input sent to the api and the cookie that is being used to authenticate with the device
  'Content-Type': 'application/json',
  'Cookie': 'APIC-cookie=' + cookie
}

response = requests.request("POST", url, headers=headers, verify=False, data=json.dumps(payload)) # repsone sends the api post call to the location specified in the url variable

print(response.text) # the response is printed from the call ensuring a 200 code is sent back ensuring the call was valid






### Question 32


import requests # import statements importing request and json libraries
import json

#getCookie was imported from the turnipTheBeet git repository

def getCookie(addr): # function responsible for renewing the authentication cookie
    

    url = "https://"+ addr + "/api/aaaLogin.json" # url contains the destination for the api call, with addr being the ip address of the
                                                  # device being passed to the function
 
    payload= {"aaaUser" : # the payload contains the username and password to authenticate with the nxos api 
              {"attributes" :
                   {"name" : "cisco",
                    "pwd" : "cisco"}
               }
          }

    response = requests.post(url, json=payload, verify = False) # repsone sends the api call to the location specified in the url variable

    return response.json()["imdata"][0]["aaaLogin"]["attributes"]["token"] # the api response is returned to the program for further use




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



def validHostname(hostname): #Function validating user input hostname
    validHost = False #Flag measuring if the hostname is valid or not

    #If statement Checking for alpha characters in the first character of the hostname, no spaces in the hostname,
    #and hostname for 64 or less characters.
    if hostname[0].isalpha() == True and hostname.count(' ') == 0 and len(hostname) <= 64:
        validHost = True
    else:
        validHost = False 
                        
    return validHost # validHost returned to main for further use





def sendToTS(authCookie,IP,Hostname): # function responsible for sending dme model changing the hostname to a nxos device

    url = "https://" + IP + "/api/node/mo/sys.xml?query-target=self" # url contains the destination for the api call, with IP being 
                                                  # the ip address of the device being passed to the function


    payload="<topSystem name="+ Hostname + "/>" # payload sends the passed hostname to overwrite name variable in the dme model

    headers ={ # headers specify the type of input sent to the api and the cookie that is being used to authenticate with the device
    'Content-Type': 'application/json',
    'Cookie': 'APIC-cookie=' + authCookie
    }

    response = requests.request("POST", url, headers=headers, verify=False, data=json.dumps(payload)) #  repsone sends the api post call to the location specified in the url variable

    return response # response is returned back to code for further use



### main code

askUser = userInput("Would you like to change a hostname on a device? [Y or N]: ", ['y','n','Y','N']) # the user is asked if they would like to
                                                                                                      # make a change to a device

if askUser.lower() == 'y': # if the user wants to make a change, the following will occur
    
    userAddress = input('Enter the address IP of the device you would like to change (x.x.x.x): ') # the user is asked for an ip address and 
    checkIP = validIP(userAddress)                                                                 # the ip is checked for validity
            
    while checkIP == False: # if the ip address is not valid the user will be asked to enter a valid ip address and the address will be rechecked
          
        print('The entered IP address is not a valid IP address.')
        userAddress = input('Enter the address IP of the device you would like to change (x.x.x.x): ')
        checkIP = validIP(userAddress)

    else: # if the ip address is valid, the user is asked what the new hostname for the device should be, and then it will be checked for validity
            
        userHost = input('Enter the hostname you would like to configure on this device: ')
        checkHost = validHostname(userHost)

    while checkHost == False: # if the hostname is not valid the user will be asked to enter a valid hostname and the hostname will be rechecked
          
        print('The entered hostname is not a valid hostname.')
        userHost = input('Enter the hostname you would like to configure on this device: ')
        checkHost = validHostname(userHost)
        
    else: # if the hostname is deemed valid the cookie variable will call the getcookie function to authenticate with the user specified address 
          # and the user specified hostname, ip address, and authentication cookie are passed to the sendToTS function to make the api call
          
        cookie = getCookie(userAddress)
        pushHostname = sendToTS(cookie,userAddress,userHost) 
        print('The device hostname was changed to ' + userHost + ' on ' + userAddress) # a print statment confirming the change was made is displayed


            
            
if askUser.lower() == 'n': # if the user doesnt want to change a device hostname, a prompt saying no changes were made is displayed 
    print('No changes were made to any devices')








