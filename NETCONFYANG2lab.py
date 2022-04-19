'''
Date: 4/16/22

Author: Chance Homme

This script is responsible for asking a user if they would like to change the ip address and subnet of an interface on a device. once the
interface, ip address and subnet mask are specified, the program will push the changes using netconf-yang in xml.

'''

from ncclient import manager # import statement importing the netconf client library


### xmlns:xc added for ios xe 17.x and greater





def changeXML(xmlInt, userAddress, userInt, userSN): # function used to modify variables in xml config
    
# Lines 30-33 were imported from the turnipTheBeet git repository

    intNumber = userInt[-1:] # intNumber stores the number of the interface
    
    intName = userInt[:-1] # intName stores the name of the interface

    # lines 30-33 are replacing the address, interface name, interface number, and subnet mask variables with user specified parameters
        
    xmlInt = xmlInt.replace("%addr%", userAddress)
    xmlInt = xmlInt.replace("%intName%", intName)
    xmlInt = xmlInt.replace("%intNum%", intNumber)
    xmlInt = xmlInt.replace("%mask%", userSN)

#    print(xmlInt) test print statment 
    
    return xmlInt # the xml config is returned to main for further use




def netconfCall(xmlInt, router): # function used to make netconf call
    
# Lines 46-45 were imported from the turnipTheBeet git repository

# with statement takes information from the device dictionary to specify the location and auth credientials of the device

    with manager.connect(host=router['host'],port=router['port'],username=router['username'],password=router['password'],hostkey_verify=False) as m:

        netconf_reply = m.edit_config(target = 'running', config = xmlInt) # netconf call is made using passed xml config and information from line 48 
        
#        print(netconf_reply) test print statment


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
    






### Main Code

# Lines 140-162 were imported from the turnipTheBeet git repository

router = {"host": "10.10.20.175", "port" : "830", # router is a dictionary that contains device information for a netconf call
      "username":"cisco","password":"cisco"}

# xmlConfig contains the model for which device changes can be made, configurable items are shown in a %word% format
xmlConfig = """<config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns = "urn:ietf:params:xml:ns:netconf:base:1.0">  
		<native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
			<interface>
                            <%intName%>
				<name>%intNum%</name>
				
				<ip>                                    
                                    <address>
                                        <primary>
                                            <address>%addr%</address>
                                            <mask>%mask%</mask>
                                         </primary>
                                    </address>                                   
				</ip>				
			    </GigabitEthernet>
			</interface>
		    
                </native>
        </config>"""     

askUser = userInput('\nWould you like to change attribuites of an interface? [Y or N]: ', ['y','n','Y','N'] )
# the user is asked if they would like to make changes to any interfaces shown

if askUser.lower() == 'n': # if the user doesnt want to make changes, a print statement shows no changes were made
    print('\nNo changes were made to the device.')


if askUser.lower() == 'y': # if the user does want to make changes, the user will be asked for the interface they would like to change and the
                           # ip address they would like the interface to have

    userInt = input('\nPlease enter the interface name you would like to modify (ex. GigabitEthernet1): ')

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
            
           changedConfig = changeXML(xmlConfig, userIP, userInt, userSN) # changedConfig calls the changeXML function passing all of the user
                                                                         # specified variables to the function along with the base xml config

           netconfCall(changedConfig, router) # the netconfCall function is called passing the changed config and the device parameters
           



















