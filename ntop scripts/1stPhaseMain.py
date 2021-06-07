# Author: Janne Lehtimäki
# e-mail: janne.lehtimaki@etteplan.com
# Company: Etteplan Finland Oy
#
# ---------------------------------------------------------------------------------
#     First phase of multi-objective-shape-optimization sample generation
# ---------------------------------------------------------------------------------
# Description:
#   Runs topology optimization and manufacturing data export routines based
#   on parameter configurations. These configurations are every possible
#   combination between channel variants and materials.
# Instructions:
#   - Edit every module's *ENV*.py to setup paths and parameters that you want to run
#     the process for. (See example -folder for hints)
#   - Make yourself AUTH.py file which includes your user credentials for
#     nTopology

from CustomBlockLauncher import CustomBlockLauncher
from FileHandler import FirstPhaseFileHandler as FileHandler
from ParameterHandler import FirstPhaseParameterHandler as ParameterHandler
from MultiProcessHelper import MultiProcessHelper

from ENVIRONMENT import PROCESS_COUNT
from CB_material.ENVmaterial import MATERIAL_CHOICES

import time
from multiprocessing import Process

def initializeFirstPhase(fileHandler, paramHandler):
    fileHandler.createFileSystem()
    paramHandler.createCadConverterParameters(fileHandler.getChannelsDict())
    paramHandler.createMaterialParameters(MATERIAL_CHOICES)
    paramHandler.createFilesystemParameterSets(
        fileHandler.getVerMajorDict(),
        fileHandler.getDirnameJSONinput(),
        fileHandler.getDirnameJSONoutput(),
        fileHandler.getDirnameMesh(),
        fileHandler.getDirnameManFactData()
    )

def threadProcessAllInputs(threadCustomBlockCases, CBcaller):
    for CustomBlockCase in threadCustomBlockCases:
        CBcaller.startNtopCLsubprocess(
            {"inputs" : CustomBlockCase["CB"]},
            CustomBlockCase["ntopcl"]["JSON_input"],
            CustomBlockCase["ntopcl"]["JSON_output"]
        )
        print("Some Subprocess finished")
    print("Some thread finished process all inputs")

def main():
    # Create class instances necessary for first phase
    fileHandler = FileHandler()
    paramHandler = ParameterHandler()
    CBcaller = CustomBlockLauncher()
    multiProcessHelper = MultiProcessHelper()
    processes = []

    # Read files and create datastructures based on **/ENV*.py settings
    initializeFirstPhase(fileHandler, paramHandler)

    # Divide parameter lists equally between processes
    processParamList = multiProcessHelper.splitInputToEqualLists(
        paramHandler.getAllInputs(), PROCESS_COUNT
    )

    for multiset in processParamList:
        p = Process(target=threadProcessAllInputs, args=[multiset, CBcaller])
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()

    return 0

if __name__ == '__main__':
    main()
