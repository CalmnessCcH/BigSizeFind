#!/usr/bin/python
import json
import sys   
import os
import traceback
from subwork import SubWork
from optparse import OptionParser
reload(sys);
sys.setdefaultencoding('utf8')
sys.setrecursionlimit(1000000)

def quickSort(lists, key, left, right):
    '''
    sort the json list by asize
    '''
    if left >= right:
        return lists
    flag = lists[left]
    low = left
    high = right
    while left < right:
        while left < right and lists[right][key] >= flag[key]:
            right -= 1
        lists[left] = lists[right]
        while left < right and lists[left][key] <= flag[key]:
            left += 1
        lists[right] = lists[left]
    lists[right] = flag
    quickSort(lists, key, low, left - 1)
    quickSort(lists, key, left + 1, high)
    return lists

def formatDirInfo(sourceList, resultList, ignore):
    '''
    format ncdu output json
    '''
    route = sourceList[0]['name']
    for index, node in enumerate(sourceList):
        if isinstance(node, dict):
            if node['name'] != route:
                node['name'] = "%s/%s" % (route, node['name'])
            if not 'asize' in node:
                node['asize'] = 0
            if index != 0 or not ignore:
                resultList.append(node) 
        elif isinstance(node, list):
            if node[0]['name'] != route:
                node[0]['name'] = "%s/%s" % (route, node[0]['name'])
            formatDirInfo(node, resultList, ignore)
        else:
            pass
    return resultList

def option():
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-p", "--path", dest="path", help="The directory to be scanned.")
    parser.add_option("-c", "--command", dest="command", default="/usr/local/bin/ncdu", help="Ncdu's path.")
    parser.add_option("-n", "--num", dest="num", type="int", default=10, help="The number of displays.")
    parser.add_option("-u", "--unit", dest="unit", default="MB", help="Size unit. MB, GB, TB")
    parser.add_option("-o", "--output", dest="output", default="/tmp/.BigSizeFind.output", help="command output file path.")
    parser.add_option("-i", "--ignore", dest="ignore", action="store_true", default=False, help="Ignore display directory.")

    options, args = parser.parse_args()
    if options.path and options.command and options.num and options.output and options.unit:
        return options.path, options.command, options.num, options.output, options.unit, options.ignore

    parser.error("parameter error.")
    parser.print_help()
    sys.exit(1)

if __name__ == '__main__':
   
    (path, command, displayNum, outputFile, unit, ignore) = option()

    commandStr = "%s -qxo- %s" % (command, os.path.realpath(path))
    worker = SubWork()
    recive = worker.start(cmd=commandStr)
    scanOutFile = "/tmp/.BigSizeFind.tmp"
    with open(scanOutFile, 'w') as fd:
        if recive['code'] == 0:
            fd.write(recive['stdout'])
        else:
            print recive['stderr']
            sys.exit(1)

    try:
        jsonStr = recive['stdout']
        sourceList = json.loads(jsonStr)[3]
        resultList = []
        resultList = formatDirInfo(sourceList, resultList, ignore)
        key = "asize"
        result = quickSort(resultList, key, 0, len(resultList) - 1)

        if unit == "MB":
            sizeUnit = 1024 ** 2
        if unit == "GB":
            sizeUnit = 1024 ** 3
        if unit == "TB":
            sizeUnit = 1024 ** 4

        for line in result[-displayNum:]:
            print "%s ===> size: %d%s" % (line['name'], line['asize']/sizeUnit, unit)

        with open(outputFile, 'w') as fd:
            fd.write(json.dumps(result))
    except Exception as e:
        print 'Exception:\n%s' % traceback.format_exc()
        sys.exit(2)
