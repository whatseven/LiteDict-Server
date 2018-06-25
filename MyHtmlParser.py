import re

from bs4 import BeautifulSoup
from ext import *

class MyHTMLParser():
    def __init__(self,vData):
        self.__Soup=BeautifulSoup(vData)

        self.__solveData()

    def __solveData(self):
        # Pronunciation
        for FayinNode in self.__Soup.select("a[class='fayin']"):
            FayinNode.img.decompose()
            del FayinNode['href']
        for FayinNode in self.__Soup.select("span[class='ei-g']"):
            for Node in FayinNode.select("span[class='z']"):
                Node.decompose()
            for Node in FayinNode.select("a:nth-of-type(2)"):
                Node.decompose()


        # Example
        for ExanpleNode in self.__Soup.select("span[class='x-g']"):
            ExanpleNode.decompose()
            del FayinNode['href']

        # Totally
        for PracpronNode in self.__Soup.select("span[class='pracpron']"):
            PracpronNode.decompose()

        # test=self.__Soup.prettify()
        pass

    def getData(self):
        self.__Soup.head.append(self.__Soup.new_tag(
            "meta",charset="UTF-8"
        ))

        return self.__Soup.prettify()


