'''
Date: 4/3/2022
Author: Chance Homme

This script is responsible for utilizing RESTCONF YANG models to pull data about a devices interfaces and
create a report showing the interface id and ip addresses for all interfaces on the device in a formatted report.

'''


import requests # import statements importing request and json libraries
import json


def getIntf(mgmtIP): # function responsible for retriveing the nested dictionary containing info on the devices interfaces 

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

    return response.json() # the response is returned in json to main for further use


def reportDict(jsonResponse): # function responsible for parsing the interface dictionary into a formatted report

    intDict = jsonResponse['ietf-interfaces:interfaces']['interface'] # intDict iterates through the jsonResponse passed to the function

    for interface in intDict: # for each interface in the intDict

        if interface['enabled'] == True: # if the enabled key has a true variable then print a statement showing the interface name and ip
                     
            print(interface['name'], '\t', interface['ietf-ip:ipv4']['address'][0]['ip'])

        else: # otherwise, print the interface name and state that there is not an address configured on the interface
            
            print(interface['name'], '\t\t', 'No Address Configured')
    



### main code

deviceIP = '10.10.20.175' # deviceIP contains the ip address of the device trying to be contacted

intDict = getIntf(deviceIP) # intDict calls the getIntf function, passing deviceIP


printIntf = reportDict(intDict) # printIntf calls the reportDict function, passing the response from intDict 




##### Response from call

'''
{'ietf-interfaces:interfaces': {'interface': [{'name': 'GigabitEthernet1', 'description': 'to port6.sandbox-backend',
'type': 'iana-if-type:ethernetCsmacd', 'enabled': True, 'ietf-ip:ipv4': {'address': [{'ip': '10.10.20.175',
'netmask': '255.255.255.0'}]}, 'ietf-ip:ipv6': {}}, {'name': 'GigabitEthernet2', 'description': 'L3 Link to core-rtr01',
'type': 'iana-if-type:ethernetCsmacd', 'enabled': True, 'ietf-ip:ipv4': {'address': [{'ip': '172.16.252.21', 'netmask': '255.255.255.252'}]},
'ietf-ip:ipv6': {}}, {'name': 'GigabitEthernet3', 'description': 'L3 Link to core-rtr02', 'type': 'iana-if-type:ethernetCsmacd', 'enabled': True,
'ietf-ip:ipv4': {'address': [{'ip': '172.16.252.25', 'netmask': '255.255.255.252'}]}, 'ietf-ip:ipv6': {}}, {'name': 'GigabitEthernet4',
'description': 'L3 Link to dist-sw01', 'type': 'iana-if-type:ethernetCsmacd', 'enabled': True, 'ietf-ip:ipv4': {'address':
[{'ip': '172.16.252.2', 'netmask': '255.255.255.252'}]}, 'ietf-ip:ipv6': {}}, {'name': 'GigabitEthernet5', 'description': 'L3 Link to dist-sw02',
'type': 'iana-if-type:ethernetCsmacd', 'enabled': True, 'ietf-ip:ipv4': {'address': [{'ip': '172.16.252.10', 'netmask': '255.255.255.252'}]},
'ietf-ip:ipv6': {}}, {'name': 'GigabitEthernet6', 'description': 'L3 Link to dist-rtr02', 'type': 'iana-if-type:ethernetCsmacd', 'enabled': True,
'ietf-ip:ipv4': {'address': [{'ip': '172.16.252.17', 'netmask': '255.255.255.252'}]}, 'ietf-ip:ipv6': {}},
{'name': 'Loopback0', 'description': 'to', 'type': 'iana-if-type:softwareLoopback', 'enabled': False, 'ietf-ip:ipv4': {}, 'ietf-ip:ipv6': {}}]}}

'''

















