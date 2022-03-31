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


def createVLAN(mgmtIP, vlan, vlanName, authCookie):

    url = 'https://' + mgmtIP + '/api/mo/sys.json'
    
    print(url,vlan,vlanName)
##    payload = {
##    "topSystem": {
##    "children": [
##      {
##        "bdEntity": {
##          "children": [
##            {
##              "l2BD": {
##                "attributes": {
##                  "fabEncap": vlan,
##                  "name": vlanName
##                  }}}]}}]}}

    payload = {
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
    print(response.json())
    return response # response is returned back to code for further use







def createSVI(mgmtIP, intName, newIP, authCookie):

    url = 'https://' + mgmtIP + '/api/mo/sys.json'


    payload = {
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
    print(response.json())
    return response # response is returned back to code for further use


def createHSRP(mgmtIP, intName, hsrpIP, hsrpID, authCookie):

    url = 'https://' + mgmtIP + '/api/mo/sys.json'


    payload = {
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
    print(response.json())
    return response # response is returned back to code for further use






def createOSPF(mgmtIP, procID, area, intName, authCookie):

    url = 'https://' + mgmtIP + '/api/mo/sys.json'


    payload = {
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
    print(response.json())
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

    return ipPlusOne # ipPlusFive is returned for further use


### main code


deviceDict = {'dist-sw01' : '10.10.20.177', 'dist-sw02' : '10.10.20.178'}



newVLAN = 'vlan-110'

newVLANName = 'testNXOS'

newNetwork = '172.16.110.1'

newHSRPGroup = '10'

newHSRPAddr = '172.16.110.1'

newOSPFArea = '0.0.0.0'

newOSPFProc = '1'

interfaceName = 'vlan 110'


for device in deviceDict:
    mgmtIP = deviceDict[device]
    cookie = getCookie(mgmtIP)
    newNetwork = addIPValue(newNetwork)
    newAddress = newNetwork + '/24'
    enterVLAN = createVLAN(mgmtIP, newVLAN, newVLANName, cookie)
    enterInt = createSVI(mgmtIP, interfaceName, newAddress, cookie)
    enterHSRP = createHSRP(mgmtIP, interfaceName, newHSRPAddr, newHSRPGroup, cookie)
    enterOSPF = createOSPF(mgmtIP, newOSPFProc, newOSPFArea, interfaceName, cookie)









    
