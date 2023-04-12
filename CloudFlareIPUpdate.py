import requests, configparser, time, json, logging, datetime
import mysql.connector
# Reading the keys from the cfauth.ini file
config = configparser.ConfigParser()
config.read('/home/afcasasfranco/Docker/Script/CloudFlareIP/cfauth.ini')

#All your DNS Zonez here & Token
zone = json.loads(config.get('zone', 'zone'))
block_no_update = json.loads(config.get('no_update', 'no_update'))
bearer_token = config.get('tokens', 'bearer_token')
zone_count = range(len(zone))
# Get the time of the IP change
now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')



#MYSQL Config
config = {
  'host':'0.0.0.0',
  'user':'root',
  'password':'153190',
  'database':'cloudflare'
}

#MySQL connect
db = mysql.connector.connect(**config)
cursor = db.cursor()

#Create Tables
try:
    cursor.execute("CREATE TABLE DNS (zoneid VARCHAR(255), register_id VARCHAR(255), name VARCHAR(255) PRIMARY KEY, ipchange BOOLEAN DEFAULT True, content VARCHAR(18))")
    cursor.execute("CREATE TABLE IP (id INT PRIMARY KEY, ip VARCHAR(20)")
    cursor.close()
except:
    cursor.close()
    
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
    zone_result = requests.get(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?page=1&per_page=200&order=type&direction=asc", headers=headers)
    zone_result = zone_result.json()['result']
    return zone_result
    
#Server IP
def my_ip():
    my_ip = requests.get("https://api.ipify.org?format=json")
    my_ip = my_ip.json()['ip']
    return my_ip
    

#Compare between server ip and cloudflare ip
def compare_ips():
    real_ip = my_ip()
    cf_ip = find_cf(0)[0]['content']
    if real_ip == cf_ip:
        time.sleep(600)
        main()
    else:
        logging.info(f"{now} - IP change from {cf_ip} to {real_ip}")
        update_ip()


def update_ip():
    for i in zone_count:
        zone_id = zone[i]
        records = range(len(find_cf(i)))
        no_update = range(len(block_no_update))
        for x in records:
            if find_cf(i)[x]['type'] == 'A':
                if find_cf(i)[x]['name'] in block_no_update:
                    pass
                else:
                    print (find_cf(i)[x]['name'])
                    payload = {'content': my_ip()}
                    record_id = find_cf(i)[x]['id']
                    # Change the IP using a PUT request\
                    requests.patch(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}", headers=headers, data=json.dumps(payload))   
#compare_ips()
    
def main():
    compare_ips()

main()
