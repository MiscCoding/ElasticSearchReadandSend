def malcodeQueryRetriever(str_dt="now-1h", pageFrom = 0, size=10, fieldandwordtoFind = [], fieldexists=""):


    query = {
        "size" : size,
        "from" : pageFrom,
        "query" : {
            "bool" : {
                "must" : [

                ],
                "should" : [

                ]

            }

        }
    }

    timeQuery = {"range" : {"timestamp" : {"gte" : str_dt}}}
    query["query"]["bool"]["must"].append(timeQuery)

    if fieldandwordtoFind and (len(fieldandwordtoFind) == 2):
        sourceNode = {"term" : {fieldandwordtoFind[0] : fieldandwordtoFind[1]}}
        query["query"]["bool"]["must"].append(sourceNode)

    if(fieldexists != ""):
        sourceNode = {"exists": {"field":fieldexists}}
        query["query"]["bool"]["must"].append(sourceNode)

    return query

def malcodeQueryRetrieverByDay(str_dt="now-1d/d", end_dt="now/d", pageFrom = 0, size=10, fieldandwordtoFind = [], fieldexists=""):


    query = {
        "size" : size,
        "from" : pageFrom,
        "query" : {
            "bool" : {
                "must" : [

                ],
                "should" : [

                ]

            }

        }
    }

    timeQuery = {"range" : {"timestamp" : {"gte" : str_dt, "lte": end_dt}}}
    query["query"]["bool"]["must"].append(timeQuery)

    if fieldandwordtoFind and (len(fieldandwordtoFind) == 2):
        sourceNode = {"term" : {fieldandwordtoFind[0] : fieldandwordtoFind[1]}}
        query["query"]["bool"]["must"].append(sourceNode)

    if(fieldexists != ""):
        sourceNode = {"exists": {"field":fieldexists}}
        query["query"]["bool"]["must"].append(sourceNode)

    return query

def initializationQuery(maxWindow = 500000):
    query = {
        "max_result_window" : maxWindow
    }
    return query