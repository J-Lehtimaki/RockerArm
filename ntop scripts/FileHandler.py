from CB_cad_converter.CadConverterParameters import CadConverterParameters as CCP
import ENVIRONMENT as ENV

import os
import glob

# Strictly handles the creation of folder structures and can be used
# to retrieve information about the project filesystem
class FirstPhaseFileHandler:
    # Param 1: 
    def __init__(self):
        self._pathToInputChannels = ENV.PATH_DIR_CHANNELS_STP_INPUT
        self._inputFileExtension = ENV.INPUT_FILE_EXTENSION
        self._pathRoot = ENV.PATH_PROJECT_ROOT
        self._dirnameSamples = ENV.DIRNAME_SAMPLES
        self._pathSampleFolder = os.path.join(self._pathRoot, self._dirnameSamples)
        self._dirnameVerMajor = []   # str[] created from input channels basename
        self._pathVerMajor = []     # str[] paths to each ver major folder in root
        self._dictsVerMajor = []     # {"basename":x,"absPath":y}[] dict list
        self._dirnameJSON = ENV.DIRNAME_JSON
        self._dirnameJSONinput = ENV.DIRNAME_INPUT_JSON
        self._dirnameJSONoutput = ENV.DIRNAME_OUTPUT_JSON
        self._dirnameMesh = ENV.DIRNAME_MESH
        self._dirnameManFactData = ENV.DIRNAME_MAN_FACT_DATA
        self._dirnameFEA = ENV.DIRNAME_FEA

    def getVerMajorDict(self): return self._dictsVerMajor
    def getPathRoot(self): return self._pathRoot
    def getDirnameJSONinput(self): return self._dirnameJSONinput
    def getDirnameJSONoutput(self): return self._dirnameJSONoutput
    def getDirnameMesh(self): return self._dirnameMesh
    def getDirnameManFactData(self): return self._dirnameManFactData
    def getDirnameFEA(self): return self._dirnameFEA

    def createFileSystem(self):
        self.createRoot()
        self.createSampleFolder()
        self.createDirnameVerMajor()
        self.createVerMajorCaseFolders()
        self.createSubfolders([
            self._dirnameMesh,
            self._dirnameFEA,
            self._dirnameManFactData,
            self._dirnameJSON,
            os.path.join(self._dirnameJSON, self._dirnameJSONinput),
            os.path.join(self._dirnameJSON, self._dirnameJSONoutput)
        ])

    def createRoot(self):
        if not os.path.exists(self._pathRoot):
            os.makedirs(self._pathRoot)

    def createSampleFolder(self):
        if not os.path.exists(self._pathSampleFolder):
            os.makedirs(self._pathSampleFolder)

    def createDirnameVerMajor(self):
        find = os.path.join(self._pathToInputChannels, self._inputFileExtension)
        for i in glob.iglob(find, recursive=False):
            self._dirnameVerMajor.append(
                i.split("\\")[-1].split(".")[0].split("_")[-1]
            )

    # Creates the folder structure which the CustomBlocks use to export
    # case by case.
    # Param1: Path to export root folder
    # Param2: name of the case folder
    def createVerMajorCaseFolders(self):
        self._pathVerMajor.clear()     # Clear contents to prevent accidental duplicates
        for dirname in self._dirnameVerMajor:
            caseFolder = os.path.join(self._pathSampleFolder,dirname)
            self._pathVerMajor.append(caseFolder)
            self._dictsVerMajor.append({
                "basename":dirname,
                "absPath":caseFolder
            })
            if not os.path.exists(caseFolder):
                os.makedirs(caseFolder)

    # Creates subfolders under the project root folder
    # Param1: str[] subfolder names
    def createSubfolders(self, subfolders):
        for sf in subfolders:
            for dir in self._pathVerMajor:
                subfolder = os.path.join(dir, sf)
                if not os.path.exists(subfolder):
                    os.makedirs(subfolder)

