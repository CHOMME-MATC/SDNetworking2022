'''
Date: 4/11/22
Author: Chance Homme

This script is responsible for exploring ordered dictionaries and introducing yang netconf api call structure.

'''

from collections import OrderedDict # import statement imports the OrderedDict library from collections


## Question 2



router1 = OrderedDict([('brand','cisco'), ('model','1941'), ('mgmtIP','10.0.0.1'),('G0/0','10.0.1.1'), # router1 is an ordered dictionary containing key value pairs
                       ('G0/1','10.0.2.1'),('G0/2','10.1.0.1')])


for dictionary in router1: # for each of the ordered key value pairs, the code will print the keys and values with key and value labels respectively
    print('Key= ' + dictionary + '\t' + 'Value= ' + router1[dictionary])





## Question 4

# lines 31-55 were imported from the turnipTheBeet git repository

interface = OrderedDict([('name', 'GigabitEthernet1'), # interface is a ordered dictionary that contains device information, some of which is in nested ordered dictionaries
                         ('description', 'to port6.sandbox-backend'),
                         ('type',OrderedDict([
                             ('@xmlns:ianaift', 'urn:ietf:params:xml:ns:yang:iana-if-type'),
                             ('#text', 'ianaift:ethernetCsmacd')
                             ])
                          ),
                         ('enabled', 'true'),
                         ('ipv4', OrderedDict([
                             ('@xmlns', 'urn:ietf:params:xml:ns:yang:ietf-ip'),
                             ('address', OrderedDict([
                                 ('ip', '10.10.20.175'),
                                 ('netmask', '255.255.255.0')
                                 ])
                              )]
                                              )
                          ),
                         ('ipv6', OrderedDict([
                             ('@xmlns', 'urn:ietf:params:xml:ns:yang:ietf-ip')]
                                              )
                          )
                         ])


print(interface['ipv4']['address']['ip'] + "\t" + interface['ipv4']['address']['netmask'])
# print statement iterating through interface and the nested ipv4 and address dictionaries to print the interface address and subnet mask

print(interface['name'] + '\t' + interface['type']['#text'] + '\t' + interface['ipv4']['address']['ip'] + '\t' + interface['ipv4']['address']['netmask'])
# print statement iterating through interface and the nested ipv4 and address dictionaries to print the interface name, interface type in text,
# interface address and subnet mask.



###Code from youtube.com/watch?v=kESU4Y8DJ2A
# lines 69-86 were imported from the turnipTheBeet git repository



import xml.etree.ElementTree as ET
import xmltodict
import xml.dom.minidom
from lxml import etree
from ncclient import manager

router = {"host": "10.10.20.175", "port" : "830", # router contains information of device which we are calling via netconf
          "username":"cisco","password":"cisco"}

# with statement calls netconf api using information contained in router, getting the ietf-interfaces dictionary from the device and formatting
# in yang, the file is then saved in the working directory
with manager.connect(host=router['host'],port=router['port'],username=router['username'],password=router['password'],hostkey_verify=False) as m:
    ip_schema = m.get_schema('ietf-interfaces')
    root=ET.fromstring(ip_schema.xml)
    yang_tree = list(root)[0].text
    f = open('ietf-interfaces.yang','w')
    f.write(yang_tree)
    f.close()





