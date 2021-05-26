import unittest
import json
from .ENVunittest import \
    PATH_CAD_CONVERTER_JSONDUMP, \
    PATH_MATERIAL_JSONDUMP, \
    PATH_FILESYSTEM_JSONDUMP

from CB_material.ENVmaterial import MATERIAL_CHOICES

from ParameterHandler import FirstPhaseParameterHandler
from FileHandler import FirstPhaseFileHandler

class CombinedFilehandlerParameterHandlerTestCase(unittest.TestCase):
    def setUp(self):
        self._FHandler = FirstPhaseFileHandler()
        self._PHandler = FirstPhaseParameterHandler()

        # Do the setup that would occur in the actual main
        self._FHandler.createFileSystem()
        self._PHandler.createCadConverterParameters(self._FHandler.getVerMajorDict())
        self._PHandler.createMaterialParameters(MATERIAL_CHOICES)
        self._PHandler.createFilesystemParameterSets()

    def testDumpCadConverterParas(self):
        ccpInputsJSON = self._PHandler.getDynamicParamsLists()["CadConverterParams"]
        with open(PATH_CAD_CONVERTER_JSONDUMP, 'w') as outfile:
            json.dump(ccpInputsJSON, outfile, indent=2)
    
    def testDumpMaterialParas(self):
        materialInputsJSON = self._PHandler.getDynamicParamsLists()["material"]
        with open(PATH_MATERIAL_JSONDUMP, 'w') as outfile:
            json.dump(materialInputsJSON, outfile, indent=2)

    def testDumpFilesystemParas(self):
        filesystemInputsJSON = self._PHandler.getDynamicParamsLists()["exportPaths"]
        with open(PATH_FILESYSTEM_JSONDUMP, 'w') as outfile:
            json.dump(filesystemInputsJSON, outfile, indent=2)

