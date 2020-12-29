import re
from gather import GatherData


# Wanted items : hostname, model name, os version, uptime, cpu %idle, mem %idle, fan, power, temperature.
class CiscoParse:
    def __init__(self, data):
        self.data = data.split('\n')

    def hostname(self):
        p = re.compile('.+[#]{1}exit')
        for i in self.data:
            m = p.search(i)
            if m:
                tmp = i.split('#')
                hostname = tmp[0]
                return hostname
        hostname = 'unknown'
        return hostname

    def dev_model(self):
        p = re.compile('^cisco WS-|Cisco WS-')
        for i in self.data:
            m = p.search(i)
            if m:
                tmp = i.split(' ')
                dev_model = tmp[1]
                return dev_model
        dev_model = 'unknown'
        return dev_model

    def os_ver(self):
        p = re.compile('IOS')
        for i in self.data:
            m = p.search(i)
            if m:
                tmp = i.split(',')
                v = re.compile('Version')
                for j in tmp:
                    s = v.search(j)
                    if s:
                        version = j.strip()
                        return version
        version = 'unknown'
        return version

    def uptime(self):
        p = re.compile('uptime|Uptime')
        for i in self.data:
            m = p.search(i)
            if m:
                tmp = i.split('is')
                uptime = tmp[-1].strip()
                return uptime
        uptime = 'unknown'
        return uptime

    def cpu_usage(self):
        p = re.compile('CPU utilization')
        for i in self.data:
            m = p.search(i)
            if m:
                i = ' '.join(i.split())
                tmp = i.split(':')
                cpu_idle = 100 - int(tmp[-1].strip('%'))
                return str(cpu_idle)
        cpu_idle = 'unknown'
        return cpu_idle

    def mem_usage(self):
        p = re.compile('Processor Pool Total:|^Total:')
        for i in self.data:
            m = p.search(i)
            if m:
                i = ' '.join(i.split())             # remove many spaces
                tmp = i.split(' ')
                total = int(tmp[-5].strip(','))
                free = int(tmp[-1])
                mem_free = int(free / total * 100)
                return str(mem_free)
        mem_free = 'unknown'
        return mem_free

    def fan(self):
        p = re.compile('Fantray|FAN')
        for i in self.data:
            m = p.search(i)
            if m:
                tmp = i.split(' ')
                fan = tmp[-1].strip('\r')
                return fan
        fan = 'unknown'
        return fan

    def temperature(self):
        p = re.compile('Chassis Temperature|TEMPERATURE')
        for i in self.data:
            m = p.search(i)
            if m:
                tp = re.compile('TEMPERATURE')
                tm = tp.search(i)
                if tm:
                    tmp = i.split(' ')
                    temperature = tmp[-1].strip('\r')
                    return temperature
                else:
                    tmp = i.split(' ')
                    temperature = tmp[-3]
                    return temperature
        temperature = 'unknown'
        return temperature

    def power_supply(self):
        ps = list()
        power_supply = str()
        p = re.compile('PS[0-9]+|POWER|Built-in')
        for i in self.data:
            m = p.search(i)
            if m:
                i = ' '.join(i.split())
                ps.append(i)
        if ps:
            power = list()
            # C3550, C2950
            p = re.compile('POWER')
            for i in ps:
                m = p.search(i)
                if m:
                    tmp = i.split(' ')
                    power.append(tmp[-1].strip())

            # C3560, C3750
            p = re.compile('Built-in')
            for i in ps:
                m = p.search(i)
                if m:
                    tmp = i.split(' ')
                    power.append(tmp[-1].strip())

            # C-4507 power supply
            p = re.compile('PS[0-9]+')
            for i in ps:
                m = p.search(i)
                if m:
                    tmp = i.split(' ')
                    status = '%s: %s, %s' % (tmp[0], tmp[-3], tmp[-2],)
                    power.append(status)

            for i in power:
                power_supply = power_supply + ' ' + i
            return power_supply
        else:
            power_supply = 'unknown'
            return power_supply


class ExosParse:
    pass


class NexusParse:
    pass


if __name__ == '__main__':
    dev_telnet = {
        'ip': '165.132.246.15', 'user': 'wroot', 'password': 'n@m17P$&iu',
        'protocol': 'telnet', 'port': 23, 'vendor': 'cisco', 'check': 1
    }
    dev_ssh = {
        'ip': '106.249.232.120', 'user': 'wadmin', 'password': '@@ysmgr2017',
        'protocol': 'ssh', 'port': 22, 'vendor': 'cisco', 'check': '1'
    }

    data = GatherData(dev_telnet).gather_telnet()
    # print(data)
    # data = GatherData(dev_ssh).gather_ssh()
    hostname = CiscoParse(data).hostname()
    dev_model = CiscoParse(data).dev_model()
    os_version = CiscoParse(data).os_ver()
    cpu = CiscoParse(data).cpu_usage()
    mem = CiscoParse(data).mem_usage()
    fan = CiscoParse(data).fan()
    temperature = CiscoParse(data).temperature()

    print(hostname)
    print(dev_model)
    print(os_version)
    print(cpu)
    print(mem)
    print(fan)
    print(temperature)
