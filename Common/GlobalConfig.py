import configparser


# Public Configurations
config_path = "..\\Config\\"
configfile = "config.ini"
path = config_path + configfile
# print(path)


class GlobalConfig(object):

    def __init__(self):
        # print("Loaded config file")
        self.cp = configparser.ConfigParser()
        self.cp.read(path)

    def getConfig(self, section, key):
        # print("Retrieved string type configurations")
        return self.cp.get(section, key)

    def getIntConfig(self, section, key):
        # print("Retrieved int type configurations")
        return self.cp.getint(section, key)

    def getBooleanConfig(self, section, key):
        # print("Retrieved boolean type configurations")
        return self.cp.getboolean(section, key)