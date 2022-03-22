'''
Author: Chance Homme
Date: 2/2/2022

This script is responsible for reformatting preexisting codes for the use of
functions, as well as creating new functions in new code examples.



'''
#============
#Question 1.
#============


def nameCheck(answerList):

    count = 0
    
    for items in answerList:
        items.isalpha()
        if items.isalpha() == True:
            count +=1
            
    if count == 2 and len(answerList) == 2:
        print("Welcome to Python", answerList[0].capitalize() + ".", answerList[1].capitalize(), "is a really interesting surname! Are you related to the famous Victoria", answerList[1].capitalize() + "?")    

    else:
        print("Error: Only type your first and last name in alphanumeric characters when prompted.")



firstLast = input("Enter your full name without your middle initail:")
nameList = list(firstLast.split())
nameCheck(nameList)




#============
#Question 2.
#============

def ntpReport(ntplist):

    print("Server Name" + '\t' + "Address")
    print('\n' + "-" * 35)

    
    for key in ntplist:
            print(key + '\t\t' + ntplist[key])
    print(" ")



#============
#Question 3.
#============

def PingPrep(iplist):

    for item in iplist:
        print("Ping " + item )






#=================================
#Main code for question 2 and 3.
#=================================

ntpServer = {
    "Server1": "221.100.250.75",
    "Server2": "201.0.113.22",
    "Server3": "58.23.191.6"
    }


ipList = []

for key in ntpServer:
        ipList.append(ntpServer[key])

ntpReport(ntpServer)
PingPrep(ipList)



#============
#Question 4.
#============


#Script objectives:
#Ping devices
#Prompt user for input
#Get device info
#Validate device info
#Update dictionary


def pingDevices(deviceDict): #Ping devices function.

    for device in deviceDict.keys(): #For loop iterates through device dictionary.

        print('Ping ' + deviceDict[device]['mgmtIP']) #print statement printing faux ping of value of mgmtIP in each nested dictionary in
                                                      #the devices dictionary


def userInput(prompt, answerList): #User input function

    answer = input(prompt) #variable that tracks the users input according to the prompt that was passed to the function.

    while answer not in answerList: #while loop that will return the initial inpuy prompt if the users answer is not valid 
        print('Please respond using a valid answer.')
        answer = input(prompt)
    
    return answer #The answer will be returned once a valid answer is entered.


def validHostname(hostname): #Function validating user input hostname
    validHost = False #Flag measuring if the hostname is valid or not

    #If statement Checking for alpha characters in the first character of the hostname, no spaces in the hostname,
    #and hostname for 64 or less characters.
    if hostname[0].isalpha() == True and hostname.count(' ') == 0 and len(hostname) <= 64:
        validHost = True
    else:
        validHost = False 
                        
    return validHost

#If the hostname is considered valid, it will be returned as true, if it is not valid, it will be returned as false.        

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
        if int(octet) < 0 or int(octet) > 255:
            validIP = False
        if int(octetList[0]) == 0:
            validIP = False
        

    return validIP



    
devices = { #dictionary containing all original devices
    "R1": {
        "type": "router",
        "hostname": "R1",
        "mgmtIP": "10.0.0.1"
        },
    "R2": {
        "type": "router",
        "hostname": "R2",
        "mgmtIP": "10.0.0.2"
        },
    "S1": {
        "type": "switch",
        "hostname": "S1",
        "mgmtIP": "10.0.0.3"
        },
    "S2": {
        "type": "switch",
        "hostname": "S2",
        "mgmtIP": "10.0.0.4"
        }
    }




print(devices)
pingDevices(devices)
addDevice = userInput('add device (y or n): ', ['y','n','N','Y'])

newDevice = {'type': '',
             'hostname': '',
             'mgmtIP': '' }


if addDevice.lower() == "y":
    validDevice = False

    if validDevice == False:
        deviceType = userInput('Is this device a switch or router? (s or r): ', ['s','r','S','R'])

        if deviceType.lower() == 's':
            newDevice['type'] = 'switch'
            

        if deviceType.lower() == 'r':
            newDevice['type'] = 'router'
            

        userHostname = input('What is the hostname of this device? ')
        validHost = validHostname(userHostname)

        while validHost == False:
            print('The entered hostname is not valid')
            userHostname = input('What is the hostname of this device? ')
            validHost = validHostname(userHostname)
            
        if validHost == True:
            newDevice['hostname'] = userHostname
            

        userIP = input('What is the management IP of this device? (Enter in x.x.x.x format): ')
        deviceIP = validIP(userIP)

        while deviceIP == False:
            print('The entered IP address is not valid')
            userIP = input('What is the management IP of this device? (Enter in x.x.x.x format): ')
            deviceIP = validIP(userIP)

        if deviceIP == True:
            newDevice['mgmtIP'] = userIP           
            validDevice = True

            if validDevice == True:
                newEntry = newDevice['hostname']
                devices[newEntry] = newDevice
                print(devices)
                pingDevices(devices)
    


            
if addDevice.lower() == 'n':
    print('No changes were made.')





