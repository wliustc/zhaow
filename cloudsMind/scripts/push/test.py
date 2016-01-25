import ConfigParser


def read_conf(section, key):
    config = ConfigParser.ConfigParser()
    config.read('conf/conf.ini')
    return config.get(section, key)

def test():
    ipCluster=read_conf('Client', 'IPCluster')
    dic=eval(ipCluster)
    for key in dic.keys():
        for ip in dic.get(key).split(','):
            print ip



def main():
    test()

if __name__ == '__main__':
    main()