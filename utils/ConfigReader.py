from xml.etree import ElementTree


class ConfigReader:
    _instance = None
    root = None

    def __new__(cls, filePath):

        if not cls._instance:
            cls._instance = super(ConfigReader, cls).__new__(cls)
            cls._instance._initialize(filePath)

        return cls._instance
    

    def _initialize(self, filePath):
        config_file = ElementTree.parse(filePath)
        self.root = config_file.getroot()

    
    def getProperty(self, key: str) -> str:
        item = key.split(".")
        TAG, name = item[0], item[1]

        datas = self.root.findall(TAG)
        value = datas[0].find(name).text
        return value
