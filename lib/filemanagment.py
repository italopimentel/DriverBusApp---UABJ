import os
from kivy.utils import platform

class FileManagment():

    homeDirectory = ""
    folderDirectory = ""
    saveFileDirectory = ""

    def __init__(self):

        if platform == "android":
            self.homeDirectory = ""
            self.folderDirectory = ""
            self.saveFileDirectory = self.folderDirectory + "save/"
        else:
            self.homeDirectory = self.__getRootDirectory()
            self.folderDirectory = self.homeDirectory
            self.saveFileDirectory = self.folderDirectory + "save\\"


    def __getRootDirectory(self):
        windowsPath = os.getcwd()  # Pega o diretório atual
        windowsPathlist = list(windowsPath)
        c = 0
        for i in range(len(windowsPathlist) - 1, 0, -1):
            if windowsPathlist[i] != "\\":
                windowsPathlist.pop(-1)
            else:
                break

        windowsPath = ""
        for c in windowsPathlist:
            windowsPath += c

        if platform != "android":
            return os.getcwd() + "\\"


    def createDirectory(self):

        try:
            if platform == "android":
                os.mkdir(self.saveFileDirectory)
                print("O diretório não existia e foi criado com sucesso")
            else:
                os.mkdir(self.saveFileDirectory)
                print("O diretório não existia e foi criado com sucesso")
        except:
            pass

    def createSaveFile(self, filename):

        try:
            f = open(self.saveFileDirectory + filename, "rb")
            f.close()
        except FileNotFoundError:
            f = open(self.saveFileDirectory + filename, "wb")
            f.close()
            print("O arquivo não existia e foi criado com sucesso")

        return True


    def writeUserInfo(self, login, password):

        if self.createSaveFile("userinfo.bin") == True:
            f = open(self.saveFileDirectory + "userinfo.bin", "wb")
            f.write(("{};{}".format(login,password)).encode())
            f.close()
        else:
            print("Ocorreu algum erro")


    def deleteUserInfo(self):

        f = open(self.saveFileDirectory + "userinfo.bin", "wb")
        f.close()


    def printUserInfo(self):
        try:
            f = open(self.saveFileDirectory + "userinfo.bin", "rb")
            print(f.read())
            f.close()
        except:
            print("Ocorreu algum erro")


    def getUserInfo(self):

        readInfo = ""
        c = ''
        counter = 0
        strLogin = ""
        strPassword = ""
        try:
            if self.createSaveFile("userinfo.bin") == True:
                f = open(self.saveFileDirectory + "userinfo.bin", "rb")
                readInfo = list(f.read().decode())

                while c != ';':
                    c = readInfo[counter]
                    if c != ';':
                        strLogin += c
                        counter += 1
                counter += 1
                while counter < len(readInfo):
                    c = readInfo[counter]
                    strPassword += c
                    counter += 1

            userInfoDic = {"login": strLogin, "password": strPassword}

            return userInfoDic

        except:
            pass

windowsfile = FileManagment()
windowsfile.createDirectory()
windowsfile.createSaveFile("userinfo.bin")
#windowsfile.writeUserInfo("italoph", "12345")
#windowsfile.printUserInfo()
#print(windowsfile.getUserInfo())