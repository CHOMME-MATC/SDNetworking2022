'''
Date: 4/26/22
Author: Chance Homme

This script is responsible for asking a user for two endpoints within the NetControllerPT network
and running flow analysis between them. Once that has been done, a list of all reachable devices will be printed
detailing any other information about the devices that is retrived from the flow analysis.
'''

import json # import statements import the json and requests libraries
import requests


#lines 16-112 were imported from the turnipTheBeet git repository

net_controller = {"name": "localhost:58000", #net_controller is used to provide the url and credentials to the DNA Center controller
                  "username": "student",   # Change the username to match the username set up in lab
                  "password": "cisco"  #Change password to match password set up in lab
                  }


def get_ticket(controller,username,password): # function responsible for getting the auth ticket
    
    api_url = "http://{}/api/v1/ticket".format(controller) # api url is used to store the url of the DNA Controller

    headers = { # headers specifies the data being requested
        "content-type": "application/json"
        }

    body_json = { # body_json passes the login credentials
        "username": username,
        "password": password
        }

    response = requests.post(api_url,json.dumps(body_json),headers=headers,verify=False) # response is used to make the api call


    response_json = response.json() # response_json turns the call response into json format

    ticket = response_json["response"]["serviceTicket"] # the ticket variable stores the authentication ticket from the response_json dictionary


    return ticket # ticket is returned to main for further use




def get_hosts(cont,auth_ticket): # function responsible for getting the pc information
    
    host_url="http://{}/api/v1/host".format(cont) # host_url is used to store the url of the DNA Controller

    headers = {"X-Auth-Token": auth_ticket} # headers specifies the data being requested

    response = requests.get(host_url,headers=headers,verify=False) # response is used to make the api call 


    hosts=response.json()["response"] # hosts contains the response formatted in json from the initial call

    return hosts # hosts is returned to main for further use

def get_devices(cont, auth_ticket): # function responsible for getting the device information
    
    host_url="http://{}/api/v1/network-device".format(cont) # host_url is used to store the url of the DNA Controller

    headers = {"X-Auth-Token":auth_ticket} # headers specifies the data being requested

    response = requests.get(host_url,headers=headers,verify=False) # response is used to make the api call


    devices=response.json()["response"] # devices contains the response formatted in json from the initial call
    return devices # devices is returned to main for further use


def get_single_device(cont,auth_ticket,dev_id): # function responsible for getting the device information from a single device

    host_url="http://{}/api/v1/network-device/{}".format(cont,dev_id) # host_url is used to store the url of the DNA Controller

    headers = {"X-Auth-Token":auth_ticket} # headers specifies the data being requested

    response = requests.get(host_url,headers=headers,verify=False) # response is used to make the api call

    return response.json() # the response is returned in json to main for further use


def run_flow_analysis(cont,auth_ticket,source_ip, destination_ip):# function responsible for providing flow analysis
    
    base_url = "http://{}/api/v1/flow-analysis".format(cont) # base_url is used to store the url of the DNA Controller

    headers = {"X-Auth-Token":auth_ticket} # headers specifies the data being requested

    # initiate flow analysis
    body = {"destIP": destination_ip, "sourceIP": source_ip} # body stores the destination and source ip addresses

    initiate_response = requests.post(base_url, headers=headers, verify=False, json=body) # initiate_response creates the inital api call 
    
    flowAnalysisId = initiate_response.json()["response"]["flowAnalysisId"] # flowAnalysisId contains the flowanalysisID value from initiate_response

    detail_url = base_url + "/{}".format(flowAnalysisId) # detail_url creates a new url appending the flowAnalysisId to the base_url

    detail_response = requests.get(detail_url, headers=headers, verify=False) # detail_response makes a new api call using the detail_url

    while not detail_response.json()["response"]["request"]["status"] == "COMPLETED":  # noqa: E501 

        print("Flow analysis not complete yet, waiting 5 seconds")

        sleep(5)

        detail_response = requests.get(detail_url, headers=headers,verify=False)  # detail_response creates a new api call incase the other one times out


    # Return the flow analysis details
    return detail_response.json()["response"]
     


def printFlow(flow,cont,auth_ticket,get_single_device): # function responsible for printing the detailed flow analysis

    print('\nName' + '\t\t\t' + 'Type' + '\t\t\t' + 'Platform' + '\t\t\t' + 'Status' + '\t\t\t\t' + 'Mnged IP' + '\t\t\t\t' + 'Uptime') # print statements print out the headers and dividing line

    print( '-' * 185)


    for device in flow['networkElementsInfo']: # for each device in the flow analysis

        if device['name'].startswith('PC'): # if the device is a pc, the device['name'] and device['ip'] are printed allong with the hard coded type variable lined up to the headers

            print(device['name'] + '\t\t\t' +  'PC' + '\t\t\t' + '\t\t\t\t' + '\t\t\t\t' + device['ip'] + '\t\t' + ' ')

        else: # if the device is not a pc, data uses the device['id'] to use the get_single_device function to retrive additional information about the device
            
            data = get_single_device(cont,auth_ticket,device['id'])

            if device['name'].startswith('Router'): # if the device is a router, the device['name'], device['type'], data['productId'], data['reachabilityStatus'], device['ip'], and data['upTime'] values are printed lining up with the headers
        
                print(device['name'] + '\t\t\t' +  device['type'] + '\t\t\t' + data['productId'] + '\t\t\t\t' + data['reachabilityStatus'] + '\t\t\t' + device['ip'] + '\t\t\t\t' +  data['upTime'])

            else: # if the device is any other type, the device['name'], device['type'], data['productId'], data['reachabilityStatus'], device['ip'], and data['upTime'] values are printed lining up with the headers

                print(device['name'] + '\t\t\t' +  device['type'] + '\t' + data['productId'] + '\t\t\t' + data['reachabilityStatus'] + '\t\t\t' + device['ip'] + '\t\t\t\t' +  data['upTime'])     

    


### Main Script

# lines 148-153 are imported from the turnipTheBeet git repository

controller = net_controller["name"] #URL from Dictionary defined above
username = net_controller["username"]  #Username from Dictionary defined above
password = net_controller["password"]   #Password from Dictionary defined above
serviceTicket = get_ticket(controller,username,password) # service ticket calls the get_ticket function, passing controller, username and password

hosts = get_hosts(controller,serviceTicket) # hosts calls the get_hosts function, passing controller, and serviceTicket

ipList = [] # ipList is an empty list to contain all device IP addresses

for pc in hosts: # for each of the pc's contained in the hosts response, each of the ip addresses stored in pc['hostIp'] will be appended to the ipList

        ipList.append(pc['hostIp']) 
                
devices=get_devices(controller,serviceTicket) # devices calls the get_devices function, passing controller, and serviceTicket

for device in devices: # for each device contained in the devices response, each of the ip addresses stored in the lists contained in device['ipAddresses'] will be appended to the ipList
        
        for item in device['ipAddresses']: 
            
            ipList.append(item)


# print statements introduce the purpose of the function and list the contents of ipList
print('Welcome to the flow analysis script. This script measures the flow analysis of two endpoints displaying the devices along the path and any attributes of the devices along the path.') 
print('Here is a list of the following devices authenticated with the DNA Center: ')
print(ipList)
userStartpoint = input('\nEnter the IP address of the startpoint device: ') # the user is asked to choose a startpoint ip address from the ipList

while userStartpoint not in ipList: # if the user enters a startpoint ip address not contained in the list, the user is notified and is forced to enter a valid ip address from the list
    
    print('\nThe provided address is not a valid startpoint address.')

    userStartpoint = input('\nEnter the IP address of the startpoint device: ')

if userStartpoint in ipList: # if the user enters a startpoint ip address that is in the list, the user is asked to enter a endpoint ip address from the ipList
    
    userEndpoint = input('\nEnter the IP address of the endpoint device: ')

    while userEndpoint not in ipList: # if the user enters a endpoint ip address not contained in the list, the user is notified and is forced to enter a valid ip address from the list
        
        print('\nThe provided address is not a valid endpoint address.')
        userEndpoint = input('\nEnter the IP address of the startpoint device: ')

    if userEndpoint in ipList: # if the user enters a endpoint ip address that is in the list,

        flow = run_flow_analysis(controller,serviceTicket,userStartpoint, userEndpoint) # flow calls the run_flow_analysis function, passing the controller, serviceTicket, userStartpoint, and userEndpoint variables

        printFlow(flow,controller,serviceTicket,get_single_device) # the printFlow function is called passing the flow, controller, serviceTicket variables and the get_single_device function






            
