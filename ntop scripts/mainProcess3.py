# Author: Janne Lehtimäki
# e-mail: janne.lehtimaki@etteplan.com
# Company: Etteplan Finland Oy
# License: MIT (part of thesis work for Wärtsilä)

import time
import os

import glob

from pathlib import Path
from multiprocessing import Process, Lock
import ENVIRONMENT
from SharedResourceManager import SharedResourceManager
from colors import Style
from nTopCall3 import TopologyCaller


PROCESS_COUNT = ENVIRONMENT.PROCESS_COUNT   # Change this according to your preferenced core count

def printWelcomeMessage():
    os.system("")   # Enable colors in terminal for monitoring
    print('{s}This is main test for multiprocessing{e}'
        .format(s=Style.CYAN, e=Style.RESET))

#   Returns list of .stp files in the argument folder and it's subfolders
def folderContentStep(dir):
    existingVersions = []
    regexPath = dir + '/**/' + '*.stp'
    # Add all files names to list that was found
    for file in glob.iglob(regexPath, recursive=True):
        existingVersions.append(str(os.path.basename(file)))
    return existingVersions

# Param1: [][] filenames for each process
def startProcesses(processFileLists, topCaller):
    processes = []
    for fileSet in processFileLists:
        t = Process(target=handleFileList, args=[fileSet, topCaller])
        print("process ID", fileSet)    # Debug 2
        processes.append(t)
        t.start()
    for p in processes:
        p.join()

def startOnlySubprocesses(processFileLists, topCaller):
    for fileSet in processFileLists:
        handleFileList(fileSet, topCaller)

def handleFileList(fileSet, topCaller):
    for inputFileName in fileSet:
        l = len(inputFileName)
        if(inputFileName):
            inputLO = str(os.path.join(ENVIRONMENT.DIR_PARAM_STP_INPUT, inputFileName)),
            output = str(os.path.join(ENVIRONMENT.DIR_OUTPUT_PARASOLID, inputFileName)),
            iJson = str(Path(os.path.join(ENVIRONMENT.DIR_INPUT_JSON, f'{inputFileName[0:l-4]}_INPUT_NTOP.json'))),
            oJson = str(Path(os.path.join(ENVIRONMENT.DIR_OUTPUT_JSON, f'{inputFileName[0:l-4]}_OUTPUT_NTOP.json')))
            topCaller.subProcessRockerArm( inputLO, output, iJson, oJson)

def colorPrint(processID, msg):
    colorsID = [Style.GREEN, Style.YELLOW, Style.RED, Style.MAGENTA]
    startC = Style.UNDERLINE
    if(processID < len(colorsID)):
        startC = colorsID[processID]
    print('{s}T{id}: {message}{e}'.format(s=startC, id=processID, message=msg, e=Style.RESET))


def main():
    printWelcomeMessage()
    topCaller = TopologyCaller()

    # Get input filenames from ./input
    stepFiles = folderContentStep(ENVIRONMENT.DIR_PARAM_STP_INPUT)

    # Make filehandler
    resourceManager = SharedResourceManager(stepFiles)

    # Equally divide files for different processes
    processFileLists = resourceManager.splitInputToEqualLists(PROCESS_COUNT)
    print("in main:", processFileLists) # DEBUG 1

    # Record time for main() to finish, invoke processes
    startTime = time.perf_counter()
    startProcesses(processFileLists, topCaller)
    finishTime = time.perf_counter()

    # TODO: Save time spent in the output
    print('{s}Main took {t} seconds to complete.{e}'.
        format(s=Style.CYAN, t=finishTime-startTime, e=Style.RESET))

if __name__ == '__main__':
    main()