# --------------------------------------------------------------------------------
#                      1. Custom Material (TO_material)
# --------------------------------------------------------------------------------
# Topology optimization is to be done with 2 different materials Wärtsilä uses
# and has fatigue tests done. The fatigue limits are needed at validation phase,
# which is performed with other application written in C++. Materials are:
# - Inconel 718, at 20C >> fatigue limit 240 MPa
# - 316L EOS  >> fatigue limit: 134,5 MPa
#
# Material:             Inconel 718     316L-0410
# Printer:              ?               EOS
# Heat treatment:       As built        As built
# Cycles:               1.00E+09        1.00E+06
# runout:               yes             ?
# fail:                 no              ?
# Amplitude:            >240 Mpa        134.5 MPa
# Young's modulus (z):                  158 GPa         
# Poisson's ratio:      ?               ?

from .ENVmaterial import CB_MATERIAL

class MaterialParameters:
    def __init__(self):
        pass

    # Returns material parameter list of dicts, suitable for dumping
    # it into JSON nTopCL will use in input.json
    def getMaterialByID(self, material_ID):
        youngsModulus = {
            "name" : "youngs_modulus",
            "type" : "scalar",
            "values" : CB_MATERIAL[material_ID]["youngsModulus"]["values"],
            "units" : CB_MATERIAL[material_ID]["youngsModulus"]["units"]
        }
        poissonsRatio = {
            "name" : "poissons_ratio",
            "type" : "scalar",
            "values" : CB_MATERIAL[material_ID]["poissonsRatio"]["values"]
        }
        density = {
            "name" : "density",
            "type" : "scalar",
            "values" : CB_MATERIAL[material_ID]["density"]["values"],
            "units" : CB_MATERIAL[material_ID]["density"]["units"]
        }
        return [youngsModulus, poissonsRatio, density]

    def getMaterialsByID(self, material_ID_list):
        retVal = []
        for mat in material_ID_list:
            if mat in CB_MATERIAL:
                retVal.append(self.getMaterialByID(mat))
        return retVal

    # Returns a list of lists of dicts, which are parameter lists
    # for each material choise described in file ./ENVmaterial.py
    def getAllBlockParamsJSON(self):
        retVal = []
        for mat in CB_MATERIAL:
            retVal.append(self.getMaterialByID(mat))
        return retVal
    