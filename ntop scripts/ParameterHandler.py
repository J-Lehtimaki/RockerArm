from CB_cad_converter.CadConverterParameters \
    import CadConverterParameters as CCP
from CB_manufacturing_data_exporter.ManFactDataParameters \
    import ManufacturingDataExporterParameters as MFDparams
from CB_material.MaterialParameters \
    import MaterialParameters as MP
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
        self._filesystemParameters = [] # includes values for CB and nTopCL
        self._CCP = CCP()
        self._MFDP = MFDparams()
        self._MP = MP()
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
        for matParamSet in self._MP.getMaterialsByID(materialsList):
            self._dynamicParamsLists["material"].append(matParamSet)

    # Creates the filesystem parameters
    def createFilesystemParameterSets(self):
        verMajorDict = self._FPFH.getVerMajorDict()
        dirnameJSONinput = self._FPFH.getDirnameJSONinput()
        dirnameJSONoutput = self._FPFH.getDirnameJSONoutput()
        dirnameMesh = self._FPFH.getDirnameMesh()
        dirnameManFactdata = self._FPFH.getDirnameManFactData()

        for v in verMajorDict:
            dirpathMesh = os.path.join(verMajorDict, dirnameMesh)
            dirpathManFactData = os.path.join(verMajorDict, dirnameManFactdata)

            self._filesystemParameters.append({
                "CB" : [
                    {"name":"Dirpath_mesh", "type":"text", "value" : dirpathMesh},
                    {"name":"Dirpath_man_fact_data", "type":"text", "value": dirpathManFactData}
                ],
                # ntopcl parameters have to joined with basename and identifiers
                "ntopcl" : {
                    "JSON_input" : os.path.join(verMajorDict, dirnameJSONinput),
                    "JSON_output" : os.path.join(verMajorDict, dirnameJSONoutput)
                }
            })

