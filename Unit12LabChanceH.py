'''
Date: 4/20/22

Author: Chance Homme

This script is responsible for iterating through a dictionary of devices and creating a detailed report of the interfaces on the device, listing
the IP, subnet, and description of each one. The user will be asked if they would like to change an interface on the device and if they do they
will be asked to provide the backend IP of the device, the name of the interface they would like to change, and the new IP and subnet of the
interface. Once the information is collected and validated, an NETCONF call will be made pushing the user specified changes to the device.

'''


from ncclient import manager # import statements importing the netconf client, xml, and orderedDict libraries
from collections import OrderedDict
import xml.etree.ElementTree as ET
import xmltodict
import xml.dom.minidom
from lxml import etree
### xmlns:xc added for ios xe 17.x and greater



def getNETCONF(router): # function responsible for creating the NETCONF API call
    
# lines 30-50 were imported from the turnipTheBeet git repository

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
    


def changeXML(xmlInt, userAddress, userInt, userSN): # function used to modify variables in xml config
    
# Lines 152-155 were imported from the turnipTheBeet git repository

    intNumber = userInt[-1:] # intNumber stores the number of the interface
    
    intName = userInt[:-1] # intName stores the name of the interface

    # lines 152-155 are replacing the address, interface name, interface number, and subnet mask variables with user specified parameters
        
    xmlInt = xmlInt.replace("%addr%", userAddress)
    xmlInt = xmlInt.replace("%intName%", intName)
    xmlInt = xmlInt.replace("%intNum%", intNumber)
    xmlInt = xmlInt.replace("%mask%", userSN)

#    print(xmlInt) test print statment 
    
    return xmlInt # the xml config is returned to main for further use


def netconfCall(xmlInt, router): # function used to make netconf call
    
# Lines 168-170 were imported from the turnipTheBeet git repository

# with statement takes information from the device dictionary to specify the location and auth credientials of the device

    with manager.connect(host=router['host'],port=router['port'],username=router['username'],password=router['password'],hostkey_verify=False) as m:

        netconf_reply = m.edit_config(target = 'running', config = xmlInt) # netconf call is made using passed xml config and information from line 48 
        
#        print(netconf_reply) test print statment





### Main Code

# baseXMLconfig contains a XML template used for configuring a new ip address on a device interface

baseXMLConfig = """<config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns = "urn:ietf:params:xml:ns:netconf:base:1.0">  
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


# routers is a dictionary that contains all information needed for netconf calls on both dist-rtr devices

routers = {'dist-rtr01': {"host": "10.10.20.175", "port" : "830","username":"cisco","password":"cisco"}, 
           'dist-rtr02': {"host": "10.10.20.176", "port" : "830","username":"cisco","password":"cisco"}}

# count is a placeholder to count the order in which the devices are iterated through

count = 1

for device in routers: # for each device in the routers dictionary
    
    routerData = routers[device] # routerData contains the information needed to make a netconf call for the device

    listofInt = getNETCONF(routerData) # listofInt calls getNETCONF, passing the routerData variable

    print('\ndist-rtr0'+str(count)+': ') # a print statement displays a header for the name of the device using the count to automate the name change

    count += 1 # the count is incremented to keep the naming accurate

    printReport(listofInt) # the printReport function is called, passing the listofInt variable
    

askUser = userInput('\nWould you like to change attributes of an interface on a device? [Y or N]: ', ['y','n','Y','N'] )
# the user is asked if they would like to make changes to any interfaces on the shown devices


if askUser.lower() == 'n': # if the user doesnt want to make changes, a print statement shows no changes were made
    print('\nNo changes were made to the devices.')



if askUser.lower() == 'y': # if the user wants to change a device interface they will be asked to specify the devices backend connection IP
                           # in userDevice

    userDevice = input('Enter the IP of the device you would like to make changes to. (See GigabitEth0/1 address): ')

    configDevice = False # configDevice is a flag set to false

    for device in routers: # for each device in the routers dictionary

# if the users specified IP address is a value to one of the routers[device]['host'] dictionaries, the flag is set true, if the flag is true
# then the IP address will be checked for validity, otherwise the user will have to specify a device ip that is in the dictionary of devices.
        
        if userDevice == routers[device]['host']:

            configDevice = True

        if configDevice == True:

            validateDeviceIP = validIP(userDevice)
        
        else:

            print('The specified device is not available for NETCONF configuration')
            userDevice = input('Enter the IP of the device you would like to make changes to. (See GigabitEth0/1 address): ')

            

    while validateDeviceIP == False: # if the ip address is not valid the user will be asked to enter a valid ip address

        print('\nThe entered IP address is not a valid IP address.')
        userDevice = input('Enter the IP of the device you would like to make changes to. (See GigabitEth0/1 address): ')
        validateDeviceIP = validIP(userDevice)
        
    else:
        
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

                for device in routers: # for each device in the routers dictionary

                    if userDevice == routers[device]['host']:

# if the users specified IP address is a value to one of the routers[device]['host'] dictionaries, deviceData will contain all of the netconf
# information contained in the respecitive routers[device] dictionary


                        deviceData = routers[device]

                        changedConfig = changeXML(baseXMLConfig, userIP, userInt, userSN)
                        # changedConfig calls the changeXML function passing all of the user
                        # specified variables to the function along with the base xml config
                                                                        
                        netconfCall(changedConfig, deviceData)
                        # the netconfCall function is called passing the changed config and the parameters in deviceData
                            
                    

                    

































