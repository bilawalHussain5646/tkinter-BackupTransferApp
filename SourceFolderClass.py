class SourceFolder(object):

    def __init__(self):
        self.folderName = ""
        self.path = ""
        self.subDirectories = []
        self.data = {}
        self.directoriesLastModified = {}

    def Print(self):
        print("This is folderName:  " + self.folderName)
        print("This is folderPath:  " + self.path)
        print("This is SubDirectories:  ")
        print(self.subDirectories)
        print("This is Data :  ")
        print(self.data)
        print("This is folder with subfolder:  ")
        print(self.directoriesLastModified)

    def DeleteData(self):
        self.folderName = ""
        self.path = ""
        self.subDirectories = []
        self.data = {}
        self.directoriesLastModified = {}
