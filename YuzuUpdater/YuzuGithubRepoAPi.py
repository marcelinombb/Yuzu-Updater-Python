import requests
import py7zr
import YuzuUpdater.Contants as const
import os
import json

class YuzuUpdater:
    def __init__(self, rootPath):
        self.headers = {"Accept": "application/vnd.github.v3+json"}
        self.rootPath = rootPath
        self.lastRelease = self.getLatestRelease()

    def get(self,route):
        response = requests.get(f'{const.GITHUB_REPO}/{route}',headers=self.headers)
        return response

    def getLatestRelease(self):

        latestRelease = self.get(route="latest")

        data = latestRelease.json()

        releaseData = {
            "tag_name":data["tag_name"],
            "name":data["assets"][0]["name"],
            "download_url": data["assets"][0]["browser_download_url"]
        }

        return releaseData
    
    def createConfigFileJson(self):
        if not os.path.exists(f'{self.rootPath}/{const.CONFIG_FILENAME}'):
            self.writeOnConfigFile('{\n\t"version": "default"\n}')
            return self.openConfigFile()
        return self.openConfigFile()

    def openConfigFile(self,mode="r+"):
        return open(const.CONFIG_FILENAME, mode)
    
    def writeOnConfigFile(self,json):
        file = self.openConfigFile("w+")
        file.write(json)
        file.close()

    def readJsonConfigFile(self):
        file = self.createConfigFileJson()
        jsonDic = json.load(file)
        file.close()
        return jsonDic
        
    def checkCurrentVersion(self,configVersion):
        if self.lastRelease["tag_name"] == configVersion :
            return True
        return False

    def downloadLastRelease(self):

        lastRelease = self.lastRelease

        config = self.readJsonConfigFile()

        if self.checkCurrentVersion(config["version"]):
            print(f'Você já está atualizado versão {config["version"]}')
        else:
            self.writeOnConfigFile(f'{{\n\t"version": "{lastRelease["tag_name"]}"\n}}')

            print(f'Baixando {lastRelease["name"]}')

            data = requests.get(lastRelease["download_url"],allow_redirects=True)

            file = open(f'{self.rootPath}/{lastRelease["name"]}',"wb"); 

            file.write(data.content)

            file.close()

            self.extractFile(filename=lastRelease["name"])

            os.unlink(f'{self.rootPath}/{lastRelease["name"]}')

    def extractFile(self,filename):

        archive = py7zr.SevenZipFile(filename, mode='r')
        
        archive.extractall(path=self.rootPath)

        archive.close()
