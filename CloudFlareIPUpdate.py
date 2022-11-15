import requests, configparser, time, json, logging, datetime
import mysql.connector
# Reading the keys from the cfauth.ini file
config = configparser.ConfigParser()
config.read('cfauth.ini')

#All your DNS Zonez here & Token
zone = json.loads(config.get('zone', 'zone'))
block_update = json.loads(config.get('no_update', 'no_update'))
bearer_token = config.get('tokens', 'bearer_token')
zone_count = len(zone)
# Get the time of the IP change
now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
# Setting up the logger (a file where it records all IP changes)
logging.basicConfig(level=logging.INFO, filename='ipchanges.log', format='%(levelname)s :: %(message)s')

# The headers we want to use
headers = {
    "Authorization": f"Bearer {bearer_token}", 
    "content-type": "application/json"
    }

#Register type A save on CloudFlare from the first URL by default zone
def find_cf(i):
    zone_id = zone[i]
    zone_result = requests.get(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?page=1&per_page=20&order=type&direction=asc", headers=headers)
    zone_result = zone_result.json()['result']
    return zone_result
    
#Server IP
def my_ip():
    my_ip = requests.get("https://api.ipify.org?format=json")
    my_ip = my_ip.json()['ip']
    return my_ip
    print (my_ip)

#Compare between server ip and cloudflare ip
def compare_ips():
    real_ip = my_ip()
    cf_ip = find_cf(0)[0]['content']
    if real_ip == cf_ip:
        #You can change the waiting time its 600 seg = 10 minutes
        time.sleep(600)
        main()
    else:
        logging.info(f"{now} - IP change from {cf_ip} to {real_ip}")
        update_ip()


def update_ip():
    i = 0
    while i < zone_count:
        zone_id = zone[i]
        records = range(len(find_cf(i)))
        block = range(len(block_update))
        for x in records:
            if find_cf(i)[x]['type'] == 'A':
                for n in block:
                    if find_cf(i)[x]['name'] != block_update[n]:
                        payload = {'content': my_ip()}
                        record_id = find_cf(i)[x]['id']
                        # Change the IP using a PUT request\
                        requests.patch(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}", headers=headers, data=json.dumps(payload))
                    else:
                      pass
            else:
                pass
    
        i = i+1
    compare_ips()
    
def main():
    compare_ips()

main()
