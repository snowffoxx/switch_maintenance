import time
from telnetlib import *
from paramiko import *


cisco_cmd = [
    'terminal length 0', 'show hardware', 'show env power', 'show env temp', 'show env temp',
    'show processes cpu', 'show processes mem', 'exit',
]

exos_cmd = [
    'disable clipaging', 'show switch', 'show fan', 'show temp', 'show power', 'show cpu', 'show memory',
    'show slot', 'exit'
]


# connect, execute command, return raw data from devices.
# device format is dict type. below is example.
# {
#    'ip': '192.168.100.5', 'user': 'root', 'password': 'password',
#    'protocol': 'telnet', 'port': 23, 'vendor': 'cisco', 'check': 1,
# }
class GatherData:
    def __init__(self, device):
        self.device = device
        self.data = list()

    def gather_telnet(self):
        command = str()
        if self.device['vendor'] == 'cisco':
            cmd = cisco_cmd
        elif self.device['vendor'] == 'exos':
            cmd = exos_cmd
        else:
            messages = 'Not supported device: %s, %s' % (self.device['ip'], self.device['vendor'],)
            return messages
        if cmd:
            for i in cmd:
                command += i + '\n'
        data = str()
        try:
            tn = Telnet(host=self.device['ip'], port=self.device['port'], timeout=10)
            tn.set_debuglevel(0)
            tn.read_until(': '.encode('ascii'))                     # waiting login: prompt
            tn.write(self.device['user'].encode('ascii')+b'\n')     # send user id
            tn.read_until(':'.encode('ascii'))                      # waiting password: prompt
            tn.write(self.device['password'].encode('ascii')+b'\n') # send user password
            tn.write(command.encode('ascii')+b'\n')                 # execute command
            data = tn.read_all().decode('ascii')                    # get execute results
            tn.close()
            return data
        except Exception as ex:
            messages = 'Some error has occurred: %s %s' % (self.device['ip'], ex,)
            print(messages)
            return messages

    def gather_ssh(self):
        if self.device['vendor'] == 'cisco':
            command = cisco_cmd
        elif self.device['vendor'] == 'exos':
            command = exos_cmd
        else:
            messages = 'Not supported device: %s, %s' % (self.device['ip'], self.device['vendor'],)
            print(messages)
            return messages

        try:
            data = str()
            ssh = SSHClient()
            ssh.set_missing_host_key_policy(AutoAddPolicy())
            ssh.connect(hostname=self.device['ip'], username=self.device['user'],
                        password=self.device['password'], port=self.device['port'])
            channel = ssh.invoke_shell()
            for i in command:
                channel.send(i+'\n')
                time.sleep(0.1)
                datum = channel.recv(65535).decode('ascii')
                data += datum.replace('\r\n', '\n')
            ssh.close()
            return data
        except Exception as ex:
            messages = 'Some error has occurred: %s %s' % (self.device['ip'], ex,)
            print(messages)
            return messages


if __name__ == '__main__':
    dev_telnet = {
        'ip': '172.16.10.5', 'user': 'admin', 'password': 'yourpassword',
        'protocol': 'telnet', 'port': 23, 'vendor': 'cisco', 'check': 1
    }
    dev_ssh = {
        'ip': '192.168.100.120', 'user': 'admin', 'password': 'yourpassword',
        'protocol': 'ssh', 'port': 22, 'vendor': 'cisco', 'check': '1'
    }

    # data = GatherData(dev_telnet).gather_telnet()
    # print(data)
    data = GatherData(dev_ssh).gather_ssh()
    print(data)
