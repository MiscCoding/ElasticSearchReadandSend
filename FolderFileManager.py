import os
import OperationLogger


def makeFoldersSubFolders(DirectoryToMake=""):
    if not os.path.isdir(DirectoryToMake):
        directory = os.path.dirname(DirectoryToMake)
        try:
            os.makedirs(directory)
        except OSError as e:
            OperationLogger.logWriter("error", "Folder creation error " + e)

    else:
        OperationLogger.logWriter("warning", "Folder already exists")
        return 3


def makeLogFolderAndMoveToIt(DirectoryToMake="log/", FileToMove=""):
    relativepath = DirectoryToMake + FileToMove
    if not os.path.isdir(DirectoryToMake):
        directory = os.path.dirname(DirectoryToMake)
        try:
            os.makedirs(directory)
        except OSError as e:
            OperationLogger.logWriter("error", "Folder creation error " + e)


    else:
        OperationLogger.logWriter("warning", "Log Folder already exists")

    if not os.path.exists(relativepath):
        os.rename(FileToMove, relativepath)
    else:

        OperationLogger.logWriter("warning", "Log file already exists")
        return -4

    OperationLogger.logWriter("warning", "Log file moved successfully")
    return 0
