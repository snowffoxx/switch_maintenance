import re


# Wanted items : hostname, model name, os version, uptime, cpu %idle, mem %idle, fan, power, temperature.

class CiscoParse:
    def __init__(self, data):
        self.data = data.split('\n')

    def hosname(self):
        p = re.compile('.+[#]{1}exit')
        for i in self.data:
            m = p.search(i)
            if m:
                tmp = i.split('#')
                hostname = tmp[0]
                return hostname
        hostname = 'unknown'
        return hostname


class ExosParse:
    pass


class NexusParse:
    pass


if __name__ == '__main__':
    pass

