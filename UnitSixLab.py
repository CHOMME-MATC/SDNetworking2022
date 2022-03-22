'''
Date: 2/23/22
Author: Chance Homme

This script is responsible for sending commands to the NXAPI, parsing the output of the commands,
and the displaying the responses in formatted print statement reports.

'''


import requests
import json

def printDevices(dictionary):

    print('\n' + 'Host\t\t' + 'Type\t\t' + 'MgmtIP\t\t')
    print('\n' + "-" * 135)


    for key in dictionary: # for loop is declaring the keys of intDict[count] as seperate variables, once they are put into the temp variables,
                          # they are then checked for length requirements, if they are less than or equal to 8 characters, they will need to add
                          # a tab to line up to the column headers, once the if statements are cleared, the print statement will print each variable
                          # whilst adding a tab to space out the variables and increment the count and repeat the process until the list of dictionaries
                          # has been fully iterated through.
                          
        hostname = dictionary[key]['hostname']
        devType = dictionary[key]['deviceType']
        mgmtIP = dictionary[key]['mgmtIP']
        if len(hostname) <= 8: 
            hostname = dictionary[key]['hostname'] + '\t'

        if len(devType) <= 8:
            devtype = dictionary[key]['deviceType'] + '\t'

        print( hostname, '\t', devType, '\t', mgmtIP)




def cliCall(deviceip,command):


    """
    Modify these please
    """
    switchuser='cisco'
    switchpassword='cisco'

    url='https://'+ deviceip + '/ins'
    myheaders={'content-type':'application/json-rpc'}
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
    deviceCall = requests.post(url,data=json.dumps(payload), verify = False, headers=myheaders,auth=(switchuser,switchpassword)).json()


    response = deviceCall['result']['body'] # variable that parses response of command down to just the dictionary of the response text 

    return response
    




def showVerReport(responseDict):
    
    hostname = responseDict['host_name'] # hostname contains the hostname of the device
    
    memory = str(responseDict['memory']) # memory contains the ammount of memory on the device and is represented as a string
    
    memoryType = responseDict['mem_type'] # memoryType contains the type of data the memory integer is represented in
    
    chassis = responseDict['chassis_id']
    
    bootFile = responseDict['kick_file_name']

    
    print('\n' + 'Host\t\t' + 'Memory\t\t' + 'Chassis\t\t\t\t' + 'Boot File\t\t')
    print('\n' + "-" * 135)

    if len(hostname) <= 8: 
        hostname = responseDict['host_name'] + '\t'

    if len(memory) <= 8:
        devtype = str(responseDict['memory']) + '\t'

    if len(chassis) <= 8:
        devtype = responseDict['chassis_id'] + '\t'

    if len(bootFile) <= 8:
        devtype = responseDict['kick_file_name'] + '\t'
            
    print( hostname, '\t', memory+memoryType, '\t', chassis, '\t', bootFile, '\t')

    



def showOSPFReport(responseDict):

    condensedResponse = responseDict['TABLE_ctx']['ROW_ctx']['TABLE_nbr']['ROW_nbr']

    print('\n' + 'Router-ID\t\t' + 'Neighbor IP\t\t' + 'Interface\t\t')
    print('\n' + "-" * 135)

    count = 0
    

    
    for item in condensedResponse:

        routerID = condensedResponse[count]['rid']
    
        neighIP = condensedResponse[count]['addr'] 
    
        interface = condensedResponse[count]['intf'] 
        
        if len(routerID) <= 8: 
            hostname = condensedResponse[count]['rid'] + '\t'

        if len(neighIP) <= 8:
            devtype = condensedResponse[count]['addr'] + '\t'

        print(routerID, '\t\t', neighIP, '\t\t', interface)

        count += 1

        
        
    
  

# main code


devices = {
    'dist-sw01':
        {
        'hostname': 'dist-sw01',
        'deviceType':'switch',
        'mgmtIP':'10.10.20.177'
        },
    'dist-sw02':
        {
        'hostname': 'dist-sw02',
        'deviceType':'switch',
        'mgmtIP':'10.10.20.178'
        }
    }


deviceReport = printDevices(devices)

for device in devices:
    
   mgmtIP = devices[device]['mgmtIP']

   hostname = devices[device]['hostname']

   print('\n' + hostname+' Show Version')

   shVer = cliCall(mgmtIP,'show version')

   shVerReport = showVerReport(shVer)

   print('\n' + hostname+' Show IP OSPF Neighbors')

   shOSPF = cliCall(mgmtIP,'show ip ospf neighbors')

   shOSPFReport = showOSPFReport(shOSPF)
   



