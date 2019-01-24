import logging
import logging.handlers
import os
from datetime import datetime, timedelta


file_max_bytes = 10 * 1024 * 1024
logger = logging.getLogger("crumbs")
logger.setLevel(logging.DEBUG)

logFolder = datetime.now().strftime("%Y%m%d")
filename = 'log/' + logFolder + '/' + "ctasSender.Log"
logSubFolder = 'log/' + logFolder +'/'

if not os.path.exists(logSubFolder):
    os.makedirs(logSubFolder)

    #logging.basicConfig(filename=filename)
# fileHandler = logging.FileHandler(filename)
fileHandler = logging.handlers.RotatingFileHandler(filename=filename, maxBytes=file_max_bytes, backupCount=200)
streamHandler = logging.StreamHandler()

formatter = logging.Formatter('[%(levelname)s : %(filename)s : %(lineno)s] %(asctime)s > %(message)s ')
fileHandler.setFormatter(formatter)
streamHandler.setFormatter(formatter)

logger.addHandler(fileHandler)
logger.addHandler(streamHandler)





def logWriter(securityLevel= "warning", message=""):
    # logFolder = datetime.now().strftime("%Y%m%d")
    #
    # filename = 'log/' + logFolder + '/' + "ctasSender.Log"
    # logSubFolder = 'log/' + logFolder +'/'
    # makeFoldersSubFolders(logSubFolder)
    # logging.basicConfig(filename=filename)
    # fileHandler = logging.FileHandler(filename)
    # fileHandler.setFormatter(formatter)
    # logger.addHandler(fileHandler)

    if securityLevel == "warning":
        logger.warning(message)

    if securityLevel == "debug":
        logger.debug(message)

    if securityLevel == "info":
        logger.info(message)

    if securityLevel == "error":
        logger.error(message)

    if securityLevel == "critical":
        logger.critical(message)




def makeFoldersSubFolders(DirectoryToMake=""):
    if not os.path.exists(DirectoryToMake):
        directory = os.path.dirname(DirectoryToMake)
        try:
            os.makedirs(directory)
        except OSError as e:
            print "Folder creation error "

    else:
        print "Folder already exists"
        return 3





