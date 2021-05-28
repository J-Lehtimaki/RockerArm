    # # Makes a subprocess for nTopCL -command with parameters being:
    # # Param 1: Dict including all the CB_main inputs with correct fields
    # # Param 2: Path to save in.json -file
    # # Param 3: Path to save out.json -file
    # def subProcessRockerArm(self, blockInputs, pathJSONinput , pathJSONoutput):

# Author: Janne Lehtimäki
# e-mail: janne.lehtimaki@etteplan.com
# Company: Etteplan Finland Oy
# License: MIT (part of thesis work for Wärtsilä)
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

from CB_material.ENVmaterial import MATERIAL_CHOICES

import time
import os

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

def main():
    # Create class instances necessary for first phase
    fileHandler = FileHandler()
    paramHandler = ParameterHandler()
    CBcaller = CustomBlockLauncher()

    initializeFirstPhase(fileHandler, paramHandler)

    for set in paramHandler.getAllInputs():
        CBcaller.startNtopCLsubprocess(
            {"inputs" : set["CB"]},
            set["ntopcl"]["JSON_input"],
            set["ntopcl"]["JSON_output"]
        )

    return 0

if __name__ == '__main__':
    main()