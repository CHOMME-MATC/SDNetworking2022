'''
Date: 3/28/22
Author: Chance Homme

This script is responsible for using DME models to create a new vlan, create a new vlan interface and add an ip address to it, add an interface to
an hsrp group and add a virtual hsrp ip address, and add an interface to an ospf instance and area. This script makes these changes using a dictionary of
NXOS capable devices.

'''




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


def createVLAN(mgmtIP, vlan, vlanName, authCookie): # function responsible for creating a VLAN on devices

    url = 'https://' + mgmtIP + '/api/mo/sys.json' # url contains the destination for the api call, with mgmtIP being the ip address of the
                                                  # device being passed to the function

    payload = { # the payload iterates through the model, passing vlan and vlanName to fabEncap and name attributes respectively 
          "topSystem": {
            "children": [
              {
                "bdEntity": {
                  "children": [
                    {
                      "l2BD": {
                        "attributes": {
                          "fabEncap": vlan,
                          "name": vlanName
                        }
                      }
                    }
                  ]
                }
              }
            ]
          }
        }






    headers ={ # headers specify the type of input sent to the api and the cookie that is being used to authenticate with the device
        'Content-Type': 'text/plain',
        'Cookie': 'APIC-cookie=' + authCookie
        }
    
    response = requests.request("POST", url, headers=headers, verify=False, data=json.dumps(payload)) #  repsone sends the api post call to the location specified in the url variable

    return response # response is returned back to code for further use







def createSVI(mgmtIP, intName, newIP, authCookie): # function responsible for creating SVI config on devices

    url = 'https://' + mgmtIP + '/api/mo/sys.json' # url contains the destination for the api call, with mgmtIP being the ip address of the
                                                  # device being passed to the function


    payload = { # the payload iterates through the model, passing intName and newIP to id and addr attributes respectively 
  "topSystem": {
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
                              "id": intName
                            },
                            "children": [
                              {
                                "ipv4Addr": {
                                  "attributes": {
                                    "addr": newIP}}}]}}]}}]}}]}},{
                                        "interfaceEntity": {
                                          "children": [{
                                          "sviIf": {
                                            "attributes": {
                                              "adminSt": "up",
                                                  "id": intName}}}]}}]}}


    headers ={ # headers specify the type of input sent to the api and the cookie that is being used to authenticate with the device
        'Content-Type': 'text/plain',
        'Cookie': 'APIC-cookie=' + authCookie
        }
    
    response = requests.request("POST", url, headers=headers, verify=False, data=json.dumps(payload)) #  repsone sends the api post call to the location specified in the url variable

    return response # response is returned back to code for further use


def createHSRP(mgmtIP, intName, hsrpIP, hsrpID, authCookie): # function responsible for creating HSRP config on devices

    url = 'https://' + mgmtIP + '/api/mo/sys.json' # url contains the destination for the api call, with mgmtIP being the ip address of the
                                                  # device being passed to the function


    payload = { # the payload iterates through the model, passing intName, hsrpID, and hsrpIP to id and ip attributes respectively 
      "topSystem": {
        "children": [
          {
            "interfaceEntity": {
              "children": [
                {
                  "sviIf": {
                    "attributes": {
                      "id": intName
                    }
                  }
                }
              ]
            }
          },
          {
            "hsrpEntity": {
              "children": [
                {
                  "hsrpInst": {
                    "children": [
                      {
                        "hsrpIf": {
                          "attributes": {
                            "id": intName
                          },
                          "children": [
                            {
                              "hsrpGroup": {
                                "attributes": {
                                  "af": "ipv4",
                                  "id": hsrpID,
                                  "ip": hsrpIP,
                                  "ipObtainMode": "admin"
                                }
                              }
                            }
                          ]
                        }
                      }
                    ]
                  }
                }
              ]
            }
          }
        ]
      }
    }






    headers ={ # headers specify the type of input sent to the api and the cookie that is being used to authenticate with the device
        'Content-Type': 'text/plain',
        'Cookie': 'APIC-cookie=' + authCookie
        }
    
    response = requests.request("POST", url, headers=headers, verify=False, data=json.dumps(payload)) #  repsone sends the api post call to the location specified in the url variable

    return response # response is returned back to code for further use






def createOSPF(mgmtIP, procID, area, intName, authCookie): # function responsible for creating OSPF config on devices

    url = 'https://' + mgmtIP + '/api/mo/sys.json' # url contains the destination for the api call, with mgmtIP being the ip address of the
                                                  # device being passed to the function


    payload = { # the payload iterates through the model, passing intName, area, and procID to id, area, and name attributes respectively
    "topSystem": {
    "children": [{
        "ospfEntity": {
          "children": [{
              "ospfInst": {
                "attributes": {
                  "name": procID},
                "children": [{
                    "ospfDom": {
                      "attributes": {
                        "name": "default"},
                      "children": [{
                          "ospfIf": {
                            "attributes": {
                              "advertiseSecondaries": "yes",
                              "area": area,
                              "id": intName
                            }}}]}}]}}]}},{"interfaceEntity": {
                                "children": [{
                                "sviIf": {
                                "attributes": {
                                "id": intName}}}]}}]}}

    headers ={ # headers specify the type of input sent to the api and the cookie that is being used to authenticate with the device
        'Content-Type': 'text/plain',
        'Cookie': 'APIC-cookie=' + authCookie
        }
    
    response = requests.request("POST", url, headers=headers, verify=False, data=json.dumps(payload)) #  repsone sends the api post call to the location specified in the url variable

    return response # response is returned back to code for further use

def addIPValue(ip): # Function responsible for creating the new ip address

    seperateOctets = ip.split('.') #variable that splits the ip on the decimals for easier handling of octets
    
    octetList = [] #empty list which will contain octets       

    for octet in seperateOctets: #for loop adding all octets of the ip address to the list of octets
        octetList.append(octet)

    octetList[3] = int(octetList[3]) + 1 # The last octet of the address will be changed to an integer and have 1 added to it, after that
                                         # has been done, it will be turned back into a string and concatenated with the other octets in
                                         # octetList to be stored as one string value which is will be stored as the ipPlusFive variable

    octetList[3] = str(octetList[3])

    ipPlusOne = octetList[0]+'.'+octetList[1]+'.'+octetList[2]+'.'+octetList[3]

    return ipPlusOne # ipPlusOne is returned for further use


### main code


deviceDict = {'dist-sw01' : '10.10.20.177', 'dist-sw02' : '10.10.20.178'} # device dict contains the hostname of the devivce and the management ip of the devices



newVLAN = 'vlan-110' # newVLAN specifies the vlan that is going to be created

newVLANName = 'testNXOS' # newVLANName specifies the name of the new vlan that is going to be created

newNetwork = '172.16.110.1' # newNetwork specifies the network address that is going to be used for the SVI's created on the devices

newHSRPGroup = '10' # newHSRPGroup specifies the HSRP group number for the interface

newHSRPAddr = '172.16.110.1' # newHSRPAddr specifies the address that is used for HSRP 

newOSPFArea = '0.0.0.0' # newOSPFArea specifies the area being used for OSPF

newOSPFProc = '1' # newOSPFProc specifies the Process ID being used for OSPF

interfaceName = 'vlan 110' # interfaceName specifies the name of the interface that is going to be made on the devices


for device in deviceDict:


    mgmtIP = deviceDict[device]

    cookie = getCookie(mgmtIP)

    newNetwork = addIPValue(newNetwork)

    newAddress = newNetwork + '/24'

    enterVLAN = createVLAN(mgmtIP, newVLAN, newVLANName, cookie)

    enterInt = createSVI(mgmtIP, interfaceName, newAddress, cookie)

    enterHSRP = createHSRP(mgmtIP, interfaceName, newHSRPAddr, newHSRPGroup, cookie)

    enterOSPF = createOSPF(mgmtIP, newOSPFProc, newOSPFArea, interfaceName, cookie)


'''
for each device in the device dictionary: The value of device is declared as the management IP.cookie calls the getCookie function using the
mgmtIP variable. newNetwork is incremented by one on the fourth octet by calling addIPValue, and then is appended with the /24 subnet mask.
createVLAN is passed using mgmtIP, newVLAN, newVLANName, and cookie to make the vlan. createSVI is called by enterSVI using mgmtIP,
interfaceName, newAddress, and cookie to create the SVI of the new vlan. createHSRP is called by enterHSRP using mgmtIP, interfaceName,
newHSRPAddr, newHSRPGroup, and cookie to put the new interface in a HSRP group and add the HSRP address to the interface. createOSPF is called
by enterOSPF using mgmtIP, newOSPFProc, newOSPFArea, interfaceName, and cookie to put the SVI in OSPF process ID 1 and OSPF Area 0.
'''
