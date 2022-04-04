import requests

url = "https://10.10.20.175:443/restconf/tailf/modules/ietf-interfaces/2014-05-08"


username = 'cisco'
password = 'cisco'
payload={}
headers = {
  'Content-Type': 'application/yang-data+json',
  'Accept': 'application/yang-data+json',
  'Authorization': 'Basic cm9vdDpEX1ZheSFfMTAm'
}

response = requests.request("GET", url, auth = (username,password), verify = False, headers=headers, data=payload)

print(response.text)
