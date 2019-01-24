from pyexcel_io import save_data
from datetime import datetime, timedelta
from elasticsearch import Elasticsearch
from flask import Flask
import malCodeQuery
import subprocess
import os
import CtasAPI
import mpu.io
import TI_Name_Extractor
import FolderFileManager
import OperationLogger


app = Flask(__name__)
app.config.from_pyfile('./config.py')

es = Elasticsearch([{'host': app.config['ELASTICSEARCH_INTERNAL_IP'], 'port':app.config['ELASTICSEARCH_PORT']}])
doctype = app.config['ELASTICSEARCH_DOCTYPE']
searchIndex = app.config['CTAS_MALICIOUS_CODE_INDEX']
query = malCodeQuery.malcodeQueryRetriever(size = app.config['ELASTICSEARCH_MAX_WINDOW_SIZE'])

##Time
datenowstr = datetime.now().strftime("%Y%m%d%H%M%S")

res = ""

def elasticsearchInitialization():


    bodyQuery = malCodeQuery.initializationQuery(app.config['ELASTICSEARCH_MAX_WINDOW_SIZE'])
    res = es.indices.put_settings(index=searchIndex,
                                  body= bodyQuery
                                  )
    if res['acknowledged'] is True:
        OperationLogger.logWriter("warning", "Max window setting is done")
    else:
        OperationLogger.logWriter("error", "Error occured")


def logFileMover():
    ctasLogFileName = "CollectAPI_" + (datetime.now()-timedelta(days=1)).strftime("%Y%m%d") + ".log"
    ctasLogFolder = "log/"
    FolderFileManager.makeLogFolderAndMoveToIt(ctasLogFolder, ctasLogFileName)


def malCodeInfoReturn():
    jsonFileName = datetime.now().strftime("%Y-%m-%d-%H%M%S") +"_intel-kt" + ".json"
    folderName = "json/" + datetime.now().strftime("%Y%m%d") + "/"
    jsonFileNameAndFolderPath = folderName+jsonFileName

    # resultList = {}
    # resultList['_mal_info'] = []
    resultList = []
    UnprocessedResultList = []
    jsonToReturn = dict()
    res = es.search(index=searchIndex, doc_type=doctype, body=query)
    resResult = res['hits']['hits']
    resCount = int(res['hits']['total'])

    for row in resResult:
        singleRow = []
        singleRowInDictionary = dict()
        if 'timestamp' in row['_source']:
            singleRow.append(row['_source']['timestamp'])
            #singleRowInDictionary['timestamp'] = row['_source']['timestamp']
            singleRowInDictionary['timestamp'] = row['_source'].get('timestamp')
        else:
            singleRow.append(" ")
            singleRowInDictionary['timestamp'] = " "

        if 'target_ip' in row['_source']:
            singleRow.append(row['_source']['target_ip'])
            #singleRowInDictionary['target_ip'] = row['_source']['target_ip']
            singleRowInDictionary['target_ip'] = row['_source'].get('target_ip')
        else:
            singleRow.append(" ")
            singleRowInDictionary['target_ip'] = " "

        if 'target_port' in row['_source']:
            singleRow.append(row['_source']['target_port'])
            #singleRowInDictionary['target_port'] = row['_source']['target_port']
            singleRowInDictionary['target_port'] = row['_source'].get('target_port')
        else:
            singleRow.append(" ")
            singleRowInDictionary['target_port'] = " "

        if 'target_country' in row['_source']:
            singleRow.append(row['_source']['target_country'])
            #singleRowInDictionary['target_country'] = row['_source']['target_country']
            singleRowInDictionary['target_country'] = row['_source'].get('target_country')
        else:
            singleRow.append(" ")
            singleRowInDictionary['target_country'] = " "

        if 'mal_ip' in row['_source']:
            singleRow.append(row['_source']['mal_ip'])
            #singleRowInDictionary['mal_ip'] = row['_source']['mal_ip']
            singleRowInDictionary['mal_ip'] = row['_source'].get('mal_ip')
        else:
            singleRow.append(" ")
            singleRowInDictionary['mal_ip'] = " "

        if 'mal_url' in row['_source']:
            singleRow.append(row['_source']['mal_url'])
            #singleRowInDictionary['mal_url'] = row['_source']['mal_url']
            singleRowInDictionary['mal_url'] = row['_source'].get('mal_url')
        else:
            singleRow.append(" ")
            singleRowInDictionary['mal_url'] = " "

        if 'mal_port' in row['_source']:
            singleRow.append(row['_source']['mal_port'])
            #singleRowInDictionary['mal_port'] = row['_source']['mal_port']
            singleRowInDictionary['mal_port'] = row['_source'].get('mal_port')
        else:
            singleRow.append(" ")
            singleRowInDictionary['mal_port'] = " "

        if 'mal_country' in row['_source']:
            singleRow.append(row['_source']['mal_country'])
            #singleRowInDictionary['mal_country'] = row['_source']['mal_country']
            singleRowInDictionary['mal_country'] = row['_source'].get('mal_country')
        else:
            singleRow.append(" ")
            singleRowInDictionary['mal_country'] = " "

        if 'mal_pattern' in row['_source']:
            singleRow.append(row['_source']['mal_pattern'])
            #singleRowInDictionary['mal_pattern'] = row['_source']['mal_pattern']
            singleRowInDictionary['mal_pattern'] = row['_source'].get('mal_pattern')
        else:
            singleRow.append(" ")
            singleRowInDictionary['mal_pattern'] = " "

        if 'mal_file' in row['_source']:
            singleRow.append(row['_source']['mal_file'])
            #singleRowInDictionary['mal_file'] = row['_source']['mal_file']
            singleRowInDictionary['mal_file'] = row['_source'].get('mal_file')
        else:
            singleRow.append(" ")
            singleRowInDictionary['mal_file'] = " "

        if 'payload' in row['_source']:
            singleRow.append(row['_source']['payload'])
            #singleRowInDictionary['payload'] = row['_source']['payload']
            singleRowInDictionary['payload'] = row['_source'].get('payload')
        else:
            singleRow.append(" ")
            singleRowInDictionary['payload'] = " "

        if 'ti_name' in row['_source']:
            singleRow.append(row['_source']['ti_name'])
            #singleRowInDictionary['ti_name'] = row['_source']['ti_name']
            #singleRowInDictionary['ti_name'] = row['_source'].get('ti_name')
            singleRowInDictionary['ti_name'] = TI_Name_Extractor.Ti_Name_Extractor(row['_source'])

        else:
            singleRow.append(" ")
            singleRowInDictionary['ti_name'] = TI_Name_Extractor.Ti_Name_Extractor(row)

        if not singleRowInDictionary['ti_name']:
            pass
        else:
            resultList.append(singleRowInDictionary)

        #resultList['_mal_info'].append(singleRowInDictionary)

        #UnprocessedResultList.append(row)

    # jsonOutput = json.dumps(resultList, indent=4)
    # res = jsbeautifier.beautify(str(resultList))
    #resultList = str(resultList)
    #parsed = json.loads(resultList)
    #jsonOutput = json.dumps(parsed, indent=4)
    # with open(fileName, "w") as outfile:
    #     json.dump(jsonOutput, outfile)
    FolderFileManager.makeFoldersSubFolders(folderName)
    mpu.io.write(jsonFileNameAndFolderPath, resultList)
    # with open(fileName, "w") as outfile:
    #     json.dump(resultList, outfile)


    fileExistReturned = fileExistMethod(jsonFileNameAndFolderPath)
    if fileExistReturned == 0:
        send_fileMethod(jsonFileNameAndFolderPath)
        #logFileMover()
    else:

        OperationLogger.logWriter("warning", fileExistReturned)


def send_fileMethod(fileNameToSend):
    commandToExecute = [CtasAPI.CTAS_API_COMMAND, CtasAPI.CTAS_API_ARG, CtasAPI.CTAS_API_FILE, fileNameToSend]
    OperationLogger.logWriter("warning", "Execution parameters - " + commandToExecute )
    p = subprocess.call([CtasAPI.CTAS_API_COMMAND, CtasAPI.CTAS_API_ARG, CtasAPI.CTAS_API_FILE, fileNameToSend])

    if p == 0:
        OperationLogger.logWriter("warning", "CTAS API Executed successfully!")
    else:
        OperationLogger.logWriter("warning","Java CTAS API call failed!")

def fileExistMethod(fileNameReceived):
    currentPath = os.getcwd()
    my_file = os.path.join(currentPath, fileNameReceived)
    if os.path.exists(my_file):

        OperationLogger.logWriter("warning", "the Json File Exists")
        return 0
    else:
        res = "Json file does not Exists"
        OperationLogger.logWriter("warning", res)

        return res


def ElasticSearchDataToCtasServerPeriodically():
    OperationLogger.logWriter("warning", "ElasticSearch method called")
    elasticsearchInitialization()
    malCodeInfoReturn()
    
    

    





