'''
Author: Chance Homme

Date: 1/30/22

This script is responsible for creating and iterating through nested dictionaries.

'''

#=============================================================
#Creating and printing the contents of the nested dictionary.
#=============================================================

router1 = {
    "hostname": "R1",
    "brand": "Cisco",
    "mgmtIP": "10.0.0.1",
    "interfaces": {
        "G0/0": "10.1.1.1",
        "G0/1": "10.1.2.1"
        }
    }

print(router1.items())

print(router1.keys())

print(router1.values())

print(router1["interfaces"].items())

print(router1["interfaces"].keys())

print(router1["interfaces"].values())
      
    
#===========================================================================
#Creating an additional nested dictionary, and iterating through the nested
#values using a for loop to create a print statement with the mgmtIP keys.
#===========================================================================

devices = {
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

for keys in devices:
        print("Ping", devices[keys]["mgmtIP"])
        



























    
