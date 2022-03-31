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

    sw_url = "https://10.10.20.177/api/mo/sys.json"
    
    
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
                      "fabEncap": "vlan-110",
                      "name": "test1243"
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
    
    response = requests.request("POST", sw_url, headers=headers, verify=False, data=json.dumps(payload)) #  repsone sends the api post call to the location specified in the url variable
    print(response.json())
    return response # response is returned back to code for further use

#main

cookie = getCookie("10.10.20.177")
print(cookie)

enterVLAN = createVLAN("10.10.20.177", "vlan-110", "test12", cookie)

