# -*- coding: utf-8 -*-

import re

Ti_Name_DB = dict()
Ti_Name_DB_ByType_And_RuleName = {
    "cnc-cmd" : "명령서버(C&C)",
    '["cnc-pattern", "cnc-upo"]' : "악성코드 전파 IP 및 악성코드 전파 패턴",
    "cnc-pattern" : "악성코드 전파 패턴",
    "cnc-upo" : "악성코드 유포지 및 악성파일",
    "pos-1" : "채굴악성코드 유포지, 유포패턴, 악석파일(윈도우)",
    "ransomware" : "Ransomware(GandCrab) C&C 및 정보수집"

}

Ti_Name_DB_byMalFile_Regex = {
    "regex_rule" : ".*adb.*",
    "adb" : "채굴악성코드 유포지, 유포패턴 악성파일(안드로이드)"
}

def Ti_Name_Extractor(singleRowParameter):
    type = str(singleRowParameter['_source'].get('type'))
    mal_file = str(singleRowParameter['_source'].get('mal_file'))
    rule_name = str(singleRowParameter['_source'].get("rule_name"))
    Ti_Name_to_Return = ""

    if Ti_Name_DB_ByType_And_RuleName.get(type):
        Ti_Name_to_Return = Ti_Name_DB_ByType_And_RuleName.get(type)

    if Ti_Name_DB_ByType_And_RuleName.get(rule_name):
        Ti_Name_to_Return = Ti_Name_DB_ByType_And_RuleName.get(rule_name)

    if re.match(Ti_Name_DB_byMalFile_Regex.get('regex_rule'), mal_file) or "adb" in mal_file:
        Ti_Name_to_Return = Ti_Name_DB_byMalFile_Regex.get('adb')

    return Ti_Name_to_Return

