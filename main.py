from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from distutils.dir_util import copy_tree
import os
import stat
import time
from pathlib import Path
from SourceFolderClass import SourceFolder


# SourceFolder Object
Source = SourceFolder()

# Variables to store paths
DestinationPath = ""
DestinationArray = []
count = 0
message = ""
messageType = ""


# Colors here
headerBackgroundColor = "#323131"
backgroundColor = "#1b1b1c"
fgColor = "#f7f7f7"
footerColor = "#f7f7f7"
font = "Segoe UI"
# ----------------------------
#
# Application Information
app = Tk()
app.title("Backup Transfer App")
app.geometry("750x650")
app.iconbitmap('images/logo.ico')
app.configure(bg=backgroundColor)
# -----------------------------
#
# Title Frame
Title = Frame(app)


def fast_scandir(dirname):
    subfolders = [f.path for f in os.scandir(dirname) if f.is_dir()]
    for dirname in list(subfolders):
        subfolders.extend(fast_scandir(dirname))
    return subfolders


def ClearMessage():
    global count, message, messageType
    if count < 5:
        labelGenerate.config(text=message, foreground=messageType)
        count += 1
        app.after(1000, ClearMessage)

    elif count == 5:
        count += 1
        message = ""

        labelGenerate.config(text=message, foreground=messageType)
        app.after(1000, ClearMessage)

    else:
        count = 0


def CopyFiles():
    global message, count, messageType, labelSourceFile, labelDestinationFile
    global Source
    global DestinationPath, DestinationArray

    if (DestinationPath == "" or labelSourceFile.cget("text") == ""):
        message = "FIRST SELECT FOLDERS"
        messageType = "RED"

    else:

        # print(DestinationArray)
        try:
            for i in Source.subDirectories:

                SourcePath = Path(Source.directoriesLastModified[i])
                DestinationPathTemp = DestinationPath
                SubDirectory = str(SourcePath).split('\\')
                # print(SubDirectory)
                tempSubDirectory = SubDirectory[len(SubDirectory)-2]
                # print(tempSubDirectory)

                DestinationPathTemp += "\\"+tempSubDirectory
                if (not os.path.exists(DestinationPathTemp)):
                    os.mkdir(DestinationPathTemp)
                # print(Source.directoriesLastModified)

                tempSubDirectory = SubDirectory[len(SubDirectory)-1]
                # print(tempSubDirectory)
                DestinationPathTemp += "\\"+tempSubDirectory
                if (not os.path.exists(DestinationPathTemp)):
                    os.mkdir(DestinationPathTemp)
                # print(Source.directoriesLastModified)

                copy_tree(SourcePath, DestinationPathTemp)

                DestinationPathTemp = ""
                tempSubDirectory = ""
            message = "SUCCESS"
            messageType = "GREEN"
            labelSourceFile.config(text="")
            labelDestinationFile.config(text="")
            SourcePath = ""
            DestinationPath = ""
            Source.DeleteData()

        except:
            message = "FIRST SELECT FOLDERS"
            messageType = "RED"
    app.after(1, ClearMessage)


def labelGap(identifier, bgColor, fgcolor, msg):
    labelGenerate = ttk.Label(identifier, text=msg,
                              background=bgColor, foreground=fgcolor)
    labelGenerate.pack(pady=(0, 5))
    labelGenerate.config(font=(font, 15))


# Content Frame
Content = Frame(app, background=backgroundColor,
                width=600, height=600, pady=100)


# Left Content
LeftContent = Frame(Content, width=250, height=300,
                    background=backgroundColor)


# Right Content
RightContent = Frame(Content, width=250, height=300,
                     background=backgroundColor)

# Left Canvas
ProductCanvasLeft = Canvas(LeftContent, background=backgroundColor, width=250)
ProductCanvasLeft.pack()


# Right Canvas
ProductCanvasRight = Canvas(
    RightContent, background=backgroundColor, width=250)
ProductCanvasRight.pack()


# Footer Content
Footer = Frame(app, background=fgColor)

# Footer Canvas
FooterCanvas = Canvas(Footer, background=fgColor, width=250)
FooterCanvas.pack()


def SelectSourceFolder():
    try:
        global SourcePath, labelSourceFile, SourcePathName

        global Source
        app.filename = filedialog.askdirectory(
            title="Select Your Folder")
        source = app.filename
        SourcePath = source

        Source.path = SourcePath

        SourcePathLatest = ""
        rootdir = Source.path
        Source.subDirectories = []

        for it in os.scandir(rootdir):
            if it.is_dir():
                path = str(it.path)
                Source.subDirectories.append(path)

        for i in range(len(Source.subDirectories)):

            Source.data[Source.subDirectories[i]] = {}
            for it in os.scandir(Source.subDirectories[i]):
                fileStatsObj = os.stat(it.path)
                modificationTime = time.ctime(fileStatsObj[stat.ST_MTIME])
                temp = {it.path: modificationTime}
                Source.data[Source.subDirectories[i]].update(temp)

        for i in Source.data:

            Source.data[i] = sorted(Source.data[i].items(),
                                    key=lambda x: x[1], reverse=True)

        for i in Source.data:

            for sub in Source.data[i]:
                path = str(Path(sub[0]))

                Source.directoriesLastModified[i] = path
                break
        # print(Source.directoriesLastModified)
        Source.folderName = str(SourcePath).split('/')
        Source.folderName = Source.folderName[len(Source.folderName)-1]
        # Source.Print()

        labelSourceFile.config(text=Source.folderName)
    except:
        pass


def SelectDestinationFolder():
    try:
        global DestinationPath, labelDestinationFile, DestinationArray
        app.filename = filedialog.askdirectory(
            title="Select Your Folder")
        destination = app.filename
        DestinationPath = destination

        rootdir = DestinationPath

        DestinationArray = []

        for it in os.scandir(rootdir):
            if it.is_dir():
                # print(it.path)
                # Folders Paths Printing
                path = Path(it.path)
                temp = path
                DestinationArray.append(str(temp))

        pathd = DestinationPath.split('/')

        labelDestinationFile.config(text=pathd[len(pathd)-1])
    except:
        pass


# Title Section
label = ttk.Label(Title, text="Backup Transfer",
                  background=headerBackgroundColor, foreground=fgColor, anchor=N,)
label.config(font=(font, 40))


# Source Section Here
labelSource = ttk.Label(ProductCanvasLeft, text="Source Folder",
                        anchor=N, width=20)
labelSource.config(font=(font, 20))
labelSource.pack(fill=X, pady=(0, 50))
Button(ProductCanvasLeft, text="Select Folder",
       command=SelectSourceFolder, padx=15, pady=15).pack()


labelSourceFile = ttk.Label(ProductCanvasLeft, text="",
                            background=backgroundColor, foreground=fgColor)
labelSourceFile.pack(pady=(0, 5))
labelSourceFile.config(font=(font, 15))


# Destination Section
labelDestination = ttk.Label(ProductCanvasRight, text="Destination Folder",
                             anchor=N, width=20)
labelDestination.config(font=(font, 20))
labelDestination.pack(fill=X, pady=(0, 50))
Button(ProductCanvasRight, text="Select Folder",
       command=SelectDestinationFolder, padx=15, pady=15).pack()

labelDestinationFile = ttk.Label(ProductCanvasRight, text="",
                                 background=backgroundColor, foreground=fgColor)
labelDestinationFile.pack(pady=(0, 5))
labelDestinationFile.config(font=(font, 15))


# Footer Section


labelGenerate = ttk.Label(FooterCanvas, text="",
                          background=fgColor, foreground=backgroundColor)
labelGenerate.pack(pady=(0, 5))
labelGenerate.config(font=(font, 15))


Submit = Button(FooterCanvas, text="Transfer",
                command=CopyFiles, padx=10, pady=15, background="Green", foreground="white", width=20)
Submit.config(font=(font, 15))
Submit.pack(fill=X)

labelGap(FooterCanvas, fgColor, backgroundColor, "")
# Footer Ends Here


label.pack(fill=X)
Title.pack(fill=X)
Content.pack(fill="both", pady=(0, 50))
Footer.pack(fill=X)

LeftContent.pack(fill="both", expand="yes", side=LEFT)
RightContent.pack(fill="both", expand="yes", side=RIGHT)
app.resizable(False, False)
app.mainloop()
