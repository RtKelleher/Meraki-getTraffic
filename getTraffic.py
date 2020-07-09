import requests
import json
import sys, os

orgID = '<ORG #>'
base_url = 'https://api-mp.meraki.com/api/v0/'

headers = {
    'Accept': '*/*',
    'X-Cisco-Meraki-API-Key': '<API KEY>',
    'User-Agent': 'Your-Agent',
    'Cache-Control': 'no-cache',
    'Host': 'api.meraki.com',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Referer': 'https://api.meraki.com/api/v0/organizations/' + orgID + '/networks'
}

response = requests.get(
    base_url + 'organizations/' + orgID + '/networks',
    headers=headers)

if response.status_code == 200 or \
    response.status_code == 201:
    networkIDs = []
    for id in response.json():
        for attribute, value in id.items():
            if attribute == 'id':
                networkIDs.append(value)
    for item in networkIDs:
        clientData = requests.get(
                    base_url + '/networks/' + item + '/clients?timespan=300', #connected clients
                    headers=headers)
        with open((os.path.join('/var/log/meraki/clients/' + item + '.txt')), 'wt') as file:
            json.dump(clientData.json(), file)
        
        assocData = requests.get(
                    base_url + '/networks/' + item + '/events?productType=wireless&includedEventTypes[]=association&perPage=100', #wireless client association
                    headers=headers)
        with open((os.path.join('/var/log/meraki/association/' + item + '.txt')), 'wt') as file:
            json.dump(assocData.json()['events'], file)

        authData = requests.get(
                    base_url + '/networks/' + item + '/events?productType=wireless&includedEventTypes[]=8021x_auth&perPage=100', #wireless client authentication
                    headers=headers)
        with open((os.path.join('/var/log/meraki/wireless_authentication/' + item + '.txt')), 'wt') as file:
            json.dump(authData.json()['events'], file)
else:
    print(json.dumps(response.status_code, indent=4, sort_keys=True))

sys.exit

#todo- Check last pull, compare, prevent multiple pulls, logging
