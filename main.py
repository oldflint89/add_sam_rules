from urllib.request import urlopen
from netmiko import ConnectHandler

def get_list(url):
    'this function will generate list of objects from url'
    data_list = []
    data = urlopen(url)
    for line in data:
        data_list.append(line.decode('UTF-8').strip())
    return data_list

ip_list = get_list('https://safe-surf.ru/upload/ALRT/proxies.txt')

#change IP and credentials to the relevant one
credentials = {
        'device_type' : 'checkpoint_gaia',
        'host' : '10.77.15.133',
        'username' : 'admin',
        'password' : 'zubur1',
        }

#User must use bash shell
ssh = ConnectHandler(**credentials)
#Delete all current SAM rules
ssh.send_command('fw sam -f localhost -D')
#Add new SAM rules from ip list
for i in ip_list:
    print(f'add {i}')
    result = ssh.send_command(f'fw sam -f localhost -j src {i}')
    print(result)
ssh.disconnect()
