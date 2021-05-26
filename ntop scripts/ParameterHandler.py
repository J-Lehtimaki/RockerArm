from CB_cad_converter.CadConverterParameters \
    import CadConverterParameters as CCP
from CB_manufacturing_data_exporter.ManFactDataParameters \
    import ManufacturingDataExporterParameters as MFDparams
import ENVIRONMENT as ENV
from FileHandler import FirstPhaseFileHandler

import os

# Everything that is strictly related to forming feasible parameterset for
# the 1st phase sample generation goes here.
class FirstPhaseParameterHandler:
    def __init__(self):
        self._dynamicParamsLists = {
            "CadConverterParams" : [],  # list of lists of dicts
            "material" : [],            # list of lists of dicts
            "exportPaths" : []          # list of lists of dicts
        }
        self._staticParamsLists = []    # list of dicts
        self._allCasesParameters = []   # list of lists of dicts, all set combinations
        self._CCP = CCP()
        self._MFDP = MFDparams()
        self._FPFH = FirstPhaseFileHandler()

    def getDynamicParamsLists(self): return self._dynamicParamsLists
    def getStaticParamsLists(self): return self._staticParamsLists

    # Creates channel shape based parameters and appends to dynamic variable list
    # Param1: [{"absPath", "basename"}, ...]
    def createCadConverterParameters(self, channelListDict):
        for pair in channelListDict:
            CCparamSet = self._CCP.getBlockParamsJSON(pair["absPath"])
            self._dynamicParamsLists["CadConverterParams"].append(CCparamSet)

    # Creates material based parameters and appends to dynamic variable list
    # Param1: material_ID[<str>]
    def createMaterialParameters(self, materialsList):
        for matParamSet in self._MFDP.getMaterialsByID(materialsList):
            self._dynamicParamsLists["material"].append(matParamSet)

    # Creates the static variables for main CB what are used by nested CBs
    # Note that version major
    # Param1: List of dicts [{"verMajorDirPath"}]
    def createSampleVersioningParameterSets(self):
        pass