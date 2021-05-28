import unittest
import json
from .ENVunittest import \
    PATH_CAD_CONVERTER_JSONDUMP, \
    PATH_MATERIAL_JSONDUMP, \
    PATH_FILESYSTEM_JSONDUMP, \
    PATH_MERGED_FS_CC_JSONDUMP, \
    PATH_MERGED_FS_CC_CHID_MATID_JSONDUMP, \
    PATH_GET_ALL_TEMPLOG_1, \
    PATH_GET_ALL_TEMPLOG_2, \
    PATH_SORTED_CH_ID

from CB_material.ENVmaterial import MATERIAL_CHOICES

from ParameterHandler import FirstPhaseParameterHandler
from FileHandler import FirstPhaseFileHandler

class CombinedFilehandlerParameterHandlerTestCase(unittest.TestCase):
    def setUp(self):
        self._FHandler = FirstPhaseFileHandler()
        self._PHandler = FirstPhaseParameterHandler()

        # Do the setup that would occur in the actual main
        self._FHandler.createFileSystem()
        self._PHandler.createCadConverterParameters(self._FHandler.getChannelsDict())
        self._PHandler.createMaterialParameters(MATERIAL_CHOICES)
        self._PHandler.createFilesystemParameterSets(
            self._FHandler.getVerMajorDict(),
            self._FHandler.getDirnameJSONinput(),
            self._FHandler.getDirnameJSONoutput(),
            self._FHandler.getDirnameMesh(),
            self._FHandler.getDirnameManFactData()
        )

    def testDumpCadConverterParas(self):
        ccpInputsJSON = self._PHandler.getSortedCCparams() #getDynamicParamsLists()["CadConverterParams"]
        with open(PATH_CAD_CONVERTER_JSONDUMP, 'w') as outfile:
            json.dump(ccpInputsJSON, outfile, indent=2)

    def testDumpMaterialParas(self):
        materialInputsJSON = self._PHandler.getDynamicParamsLists()["material"]
        with open(PATH_MATERIAL_JSONDUMP, 'w') as outfile:
            json.dump(materialInputsJSON, outfile, indent=2)

    def testDumpFilesystemParas(self):
        filesystemInputsJSON = self._PHandler.getSortedFSparams() #self._PHandler.getFilesystemParameters()
        with open(PATH_FILESYSTEM_JSONDUMP, 'w') as outfile:
            json.dump(filesystemInputsJSON, outfile, indent=2)

    def testDumpMergedFilesystemCadConverter(self):
        mergedInputsJSON = self._PHandler.mergeCadConverterToFilesystem()
        with open(PATH_MERGED_FS_CC_JSONDUMP, 'w') as outfile:
            json.dump(mergedInputsJSON, outfile, indent=2)

    # CC filesystem Channel ID Material, with nTopCL .json filenames
    def testDumpMergedEverything(self):
        mergedEverything = self._PHandler.getAllInputs()
        with open(PATH_MERGED_FS_CC_CHID_MATID_JSONDUMP, 'w') as outfile:
            json.dump(mergedEverything, outfile, indent=2)

    # CC filesystem Channel ID Material, with nTopCL .json filenames
    def testDebugGetAll1(self):
        mergedEverything = self._PHandler.getCombinedMaterialChannelID()
        with open(PATH_GET_ALL_TEMPLOG_1, 'w') as outfile:
            json.dump(mergedEverything, outfile, indent=2)

    def testGetSortedChannelIDS(self):
        fSorted = self._PHandler.getSortedChannelIDS()
        t = []
        for i in fSorted:
            t.append({"chID":i})
        with open(PATH_SORTED_CH_ID, 'w') as outfile:
            json.dump(t, outfile, indent=2)
