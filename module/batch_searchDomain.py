#!/usr/bin/python3.9
# -*- coding: utf-8 -*-
# @Author : KrystianLi
# @Github : https://github.com/KrystianLi/ip2domain_modify.git

import re,os,time
import tldextract
import requests
from argParse import parseArgs

def searchDomain(ip, timeout):
    mainDomainNameList = []
    searchDomainResult = {"code": 0, "ip":ip, "domainList": []}

    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"
    }
    try:
        rep = requests.get(url=f"http://api.webscan.cc/?action=query&ip={ip}", headers=headers, timeout=timeout)
        if rep.text != "null":
            results = rep.json()
            for result in results:
                domainName = result["domain"]
                if re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", domainName):
                    continue
                if domainName  in mainDomainNameList:
                    continue
                
                mainDomainNameList.append(domainName)
            searchDomainResult["code"] = 1
            searchDomainResult["domainList"] = mainDomainNameList
        else:
            searchDomainResult["code"] = 0
    except:
        searchDomainResult["code"] = -1

    return searchDomainResult

def init(parseClass):
    args = parseClass.parse_args()
    if not args.file and not args.target:
        print(parseClass.print_usage())
        exit(0)

    if args.file:
        if not os.path.isfile(args.file):
            print(
                f"\n[\033[36m{time.strftime('%H:%M:%S', time.localtime())}\033[0m] - \033[31m[ERRO] - Load file [{args.file}] Failed\033[0m")
            exit(0)

    targetList = loadTarget(args.file, args.target)  # 所有目标

    print(
        f"[\033[36m{time.strftime('%H:%M:%S', time.localtime())}\033[0m] - \033[36m[INFO] - Timeout:   {args.timeout}s\033[0m")
    print(
        f"[\033[36m{time.strftime('%H:%M:%S', time.localtime())}\033[0m] - \033[36m[INFO] - Delay:     {args.delay}s\033[0m")
    print(
        f"[\033[36m{time.strftime('%H:%M:%S', time.localtime())}\033[0m] - \033[36m[INFO] - Rank Size: >{args.rank}\033[0m")
    print(
        f"[\033[36m{time.strftime('%H:%M:%S', time.localtime())}\033[0m] - \033[36m[INFO] - ICP:       {args.icp}\033[0m")
    print(
        f"[\033[36m{time.strftime('%H:%M:%S', time.localtime())}\033[0m] - \033[36m[INFO] - ipCount:   {len(targetList)}\033[0m\n")

    return targetList


# 加载目标
def loadTarget(file, target):
    targetList = []

    # 解析输入目标数据
    def parseData(data):
        val = tldextract.extract(data)
        if not val.suffix:
            # 校验解析的数据
            if re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
                        val.domain):
                return f"{val.domain}"
            else:
                return ""
        else:
            return f"{val.domain}.{val.suffix}"

    if file:
        f = open(file, encoding="utf8")
        for line in f.readlines():
            target_ = parseData(line.strip())
            if target_:
                targetList.append(target_)
        f.close()

    if target:
        target_ = parseData(target.strip())
        if target_:
            targetList.append(target_)

    return list(set(targetList))


if __name__ == "__main__":
    parseClass = parseArgs()
    targetList = init(parseClass)
    resultList = []
    targetCount = len(targetList)
    try:
        for i in range(len(targetList)):
            s = searchDomain(targetList[i], 3)
            if s["code"] == 1:
                for i in s["domainList"]:
                    print(f"{s['ip']}  {i}")
    except KeyboardInterrupt:
        print("\nBye~")

    
