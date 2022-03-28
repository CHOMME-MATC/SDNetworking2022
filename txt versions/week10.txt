'''
Date: 3/28/22
Author: Chance Homme

This script is responsible for iterating through a list of interfaces using DME models through the NXOS API
and printing the uri path and interface id of each interface.

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


def getInterface(authCookie,IP): # function responsible for sending a get call and returning the dme model of all the interfaces on the device

    url = 'https://'+ IP + '//api/node/mo/sys/ipv4/inst/dom-default.json?query-target=children' # url contains the destination for the api call, with IP being 
                                                  # the ip address of the device being passed to the function

    payload={} # payload is empty since no changes are being sent to the device


    headers ={ # headers specify the type of input sent to the api and the cookie that is being used to authenticate with the device
    'Content-Type': 'application/json',
    'Cookie': 'APIC-cookie=' + authCookie
    }

    response = requests.request("GET", url, headers=headers, verify=False, data=json.dumps(payload)) #  repsone sends the api get call to the location specified in the url variable
    
    return response.json() # response is returned in json back to code for further use

    

### main code

address = '10.10.20.177' # address contains the address of dist-sw01

cookie = getCookie(address) # cookie calls the getCookie function to return an authentication cookie

apiCall = getInterface(cookie,address) # apiCall calls the getInterface function to return a get response of all the interfaces on the device


for interface in apiCall["imdata"]: # for loop iterating through the top most nested dictionary in the response 
    
    print(interface['ipv4If']['attributes']['dn'] + '\t' + interface['ipv4If']['attributes']['id'])

    # print statement further iterates through the imdata dictionary to print the uri path and the interface id of each interface


