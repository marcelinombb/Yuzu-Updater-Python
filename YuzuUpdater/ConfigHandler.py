import YuzuUpdater.Contants as const
import json
import os

class ConfigHandler:
    def __init__(self, rootPath) -> None:
        self.rootPath = rootPath
    
    def createConfigFileJson(self):
        if not os.path.exists(f'{self.rootPath}/{const.CONFIG_FILENAME}'):
            self.writeOnConfigFile('{\n\t"version": "default"\n}')
            return self.openConfigFile()
        return self.openConfigFile()

    def openConfigFile(self, mode="r+"):
        return open(const.CONFIG_FILENAME, mode)

    def writeOnConfigFile(self, json):
        file = self.openConfigFile("w+")
        file.write(json)
        file.close()

    def readJsonConfigFile(self):
        file = self.createConfigFileJson()
        jsonDic = json.load(file)
        file.close()
        return jsonDic
