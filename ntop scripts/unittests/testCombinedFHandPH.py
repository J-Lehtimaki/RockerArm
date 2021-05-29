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

        self._nChannels = 36    # number of channels, container size testing
        self._nMaterials = 2    # number of materials used

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

    # def testFHsize(self):
    #     self.assertEqual(35, len(self._FHandler.getVerMajorDict()))

    # # def testSizesPhandler(self):
    # #     matChanList = self._PHandler.getCombinedMaterialChannelID()
    # #     chanIDSorted = self._PHandler.getSortedChannelIDS()
    # #     self.assertEqual(35, len(matChanList))
    # #     self.assertEqual(35, len(chanIDSorted))

    def testDumpCadConverterParas(self):
        ccpInputsJSON = self._PHandler.getSortedCCparams() #getDynamicParamsLists()["CadConverterParams"]
        self.assertEqual(self._nChannels, len(ccpInputsJSON))
        with open(PATH_CAD_CONVERTER_JSONDUMP, 'w') as outfile:
            json.dump(ccpInputsJSON, outfile, indent=2)

    def testDumpMaterialParas(self):
        materialInputsJSON = self._PHandler.getDynamicParamsLists()["material"]
        self.assertEqual(self._nMaterials, len(materialInputsJSON))
        with open(PATH_MATERIAL_JSONDUMP, 'w') as outfile:
            json.dump(materialInputsJSON, outfile, indent=2)

    def testDumpFilesystemParas(self):
        filesystemInputsJSON = self._PHandler.getSortedFSparams() #self._PHandler.getFilesystemParameters()
        self.assertEqual(self._nChannels, len(filesystemInputsJSON))
        with open(PATH_FILESYSTEM_JSONDUMP, 'w') as outfile:
            json.dump(filesystemInputsJSON, outfile, indent=2)

    def testDumpMergedFilesystemCadConverter(self):
        mergedInputsJSON = self._PHandler.mergeCadConverterToFilesystem()
        self.assertEqual(self._nChannels, len(mergedInputsJSON))
        with open(PATH_MERGED_FS_CC_JSONDUMP, 'w') as outfile:
            json.dump(mergedInputsJSON, outfile, indent=2)

    # CC filesystem Channel ID Material, with nTopCL .json filenames
    def testDumpMergedEverything(self):
        mergedEverything = self._PHandler.getAllInputs()
        self.assertEqual(self._nChannels * self._nMaterials, len(mergedEverything))
        with open(PATH_MERGED_FS_CC_CHID_MATID_JSONDUMP, 'w') as outfile:
            json.dump(mergedEverything, outfile, indent=2)

    # CC filesystem Channel ID Material, with nTopCL .json filenames
    def testDebugGetAll1(self):
        mergedEverything = self._PHandler.getCombinedMaterialChannelID()
        self.assertEqual(self._nChannels * self._nMaterials, len(mergedEverything))
        with open(PATH_GET_ALL_TEMPLOG_1, 'w') as outfile:
            json.dump(mergedEverything, outfile, indent=2)

    def testGetSortedChannelIDS(self):
        fSorted = self._PHandler.getSortedChannelIDS()
        self.assertEqual(self._nChannels, len(fSorted))
        t = []
        for i in fSorted:
            t.append({"chID":i})
        with open(PATH_SORTED_CH_ID, 'w') as outfile:
            json.dump(t, outfile, indent=2)

    def testSizeOfFinalInputs(self):
        final = self._PHandler.getAllInputs()
        nomaterial = self._PHandler.mergeCadConverterToFilesystem()
        self.assertEqual(len(final), 2*len(nomaterial))

