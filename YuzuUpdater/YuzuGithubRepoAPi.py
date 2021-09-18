import requests
import py7zr
import YuzuUpdater.Contants as const
import os

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

    def downloadLastRelease(self):

        lastRelease = self.lastRelease

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
