from CB_cad_converter.CadConverterParameters \
    import CadConverterParameters as CCP
from CB_manufacturing_data_exporter.ManFactDataParameters \
    import ManufacturingDataExporterParameters as MFDparams
from CB_material.MaterialParameters \
    import MaterialParameters as MP

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
        self._filesystemParameters = [] # includes values for CB and nTopCL
        self._CCP = CCP()
        self._MFDP = MFDparams()
        self._MP = MP()

    def getDynamicParamsLists(self): return self._dynamicParamsLists
    def getFilesystemParameters(self): return self._filesystemParameters

    def getSortedFSparams(self): return sorted(
        self._filesystemParameters, key = lambda i: 
            int(i["CB"][0]["value"].split("\\")
                [len(i["CB"][0]["value"].split("\\")) - 2]
            )
    )

    def mergeCadConverterToFilesystem(self):
        retval = []
        fSorted = self.getSortedFSparams()
        cSorted = self.getSortedCCparams()

        if(len(fSorted) == len(cSorted)):
            for i in range(0, len(fSorted)-1):
                retval.append({
                    "CB" : fSorted[i]["CB"] + cSorted[i],
                    "ntopcl" : fSorted[i]["ntopcl"]
                })
            return retval

    def getSortedChannelIDS(self):
        fSorted = self.getSortedFSparams()
        idList = []
        for i in fSorted:
            idList.append(int(
                i["CB"][0]["value"].split("\\")[len(i["CB"][0]["value"].split("\\")) - 2]
                )
            )
        idList.sort()
        return idList

    def getCombinedMaterialChannelID(self):
        retval = []
        materials = self._dynamicParamsLists["material"]
        channelIDs = self.getSortedChannelIDdict()
        for mlist in materials:
            for id in channelIDs:
                retval.append([mlist[0], mlist[1], mlist[2], mlist[3], id])
        return retval

    def getSortedChannelIDdict(self):
        retval = []
        idList = self.getSortedChannelIDS()
        for id in idList:
            retval.append({"name" : "channel_ID", "type" : "text", "value" : str(id)})
        return retval

    def getAllInputs(self):
        retval = []
        materialChannelsIDList = self.getCombinedMaterialChannelID()
        mergedFSandCCList = self.mergeCadConverterToFilesystem()
        j=int(len(mergedFSandCCList)) + 1  #index materialchanlist (two materials, chanIDs ascending)
        for i in range(0, len(mergedFSandCCList)-1):
            retval.append({
                "CB": mergedFSandCCList[i]["CB"] + materialChannelsIDList[i],
                "ntopcl":{
                    "JSON_input": 
                        "{path}\\{chID}_{mID}_input.json".format(
                            path=mergedFSandCCList[i]["ntopcl"]["JSON_input"],
                            chID=materialChannelsIDList[i][4]["value"],
                            mID=materialChannelsIDList[i][3]["value"]
                        ),
                    "JSON_output":
                        "{path}\\{chID}_{mID}_output.json".format(
                            path=mergedFSandCCList[i]["ntopcl"]["JSON_output"],
                            chID=materialChannelsIDList[i][4]["value"],
                            mID=materialChannelsIDList[i][3]["value"]
                        )
                }
            })
            retval.append({
                "CB": mergedFSandCCList[i]["CB"] + materialChannelsIDList[j],
                "ntopcl":{
                    "JSON_input": 
                        "{path}\\{chID}_{mID}_input.json".format(
                            path=mergedFSandCCList[i]["ntopcl"]["JSON_input"],
                            chID=materialChannelsIDList[j][4]["value"],
                            mID=materialChannelsIDList[j][3]["value"]
                        ),
                    "JSON_output":
                        "{path}\\{chID}_{mID}_output.json".format(
                            path=mergedFSandCCList[i]["ntopcl"]["JSON_output"],
                            chID=materialChannelsIDList[j][4]["value"],
                            mID=materialChannelsIDList[j][3]["value"]
                        )
                }
            })
            j+=1
        return retval

    # Returns sorted [][]{} based on dict <key> "basename" : <val> abspath
    # example "C:\\my\\fake\\path\\urho_kekkonen_123123.stp"
    #                                            ^^^^^^
    def getSortedCCparams(self):
        return sorted(
            self._dynamicParamsLists["CadConverterParams"],
            key = lambda i:
                int(i[["Path_LO_channels" in j["name"] for j in i].index(True)]
                    ["value"].split("\\")[-1].split(".")[0].split("_")[-1]
                )
        )

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
    # Param1: use FileHandler.getVerMajorDict()
    # Param2: use FileHandler.getDirnameJSONinput()
    # Param3: use FileHandler.getDirnameJSONoutput()
    # Param4: use FileHandler.getDirnameMesh()
    # Param5: use FileHandler.getDirnameManFactData()
    def createFilesystemParameterSets(self, a, b, c, d, e):
        verMajorDict = a
        dirnameJSONinput = b
        dirnameJSONoutput = c
        dirnameMesh = d
        dirnameManFactdata = e  

        for v in verMajorDict:
            dirpathMesh = os.path.join(v["absPath"], dirnameMesh)
            dirpathManFactData = os.path.join(v["absPath"], dirnameManFactdata)

            self._filesystemParameters.append({
                "CB" : [
                    {"name":"Dirpath_mesh", "type":"text", "value" : dirpathMesh},
                    {"name":"Dirpath_man_fact_data", "type":"text", "value": dirpathManFactData}
                ],
                # ntopcl parameters have to joined with basename and identifiers
                # to identify material and version number "ver_material.json"
                "ntopcl" : {
                    "JSON_input" : os.path.join(v["absPath"], "nTop_JSON", dirnameJSONinput),
                    "JSON_output" : os.path.join(v["absPath"], "nTop_JSON", dirnameJSONoutput)
                }
            })

