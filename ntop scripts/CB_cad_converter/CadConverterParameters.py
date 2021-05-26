# ----------------------------------------------------------------------------------
#   	                        0. CB_CAD_converter
# ----------------------------------------------------------------------------------
# NOTE: Currently only channels are thought to be varied.
# NOTE: All paths are are to solid bodies EXCEPT 1 PR_cyl_surf_bottom -surface .
#   Path_LO_channels    (dynamic)
#   Path_DS
#   Path_machining      (PR, pin, V united in .stp input)
#   Path_PR_bushing_enclosed
#   Path_PR_hole_inverse
#   Path_PR_machining_allowance
#   Path_PR_passive_region_booster
#   Path_PR_cyl_surf_bottom
#   Path_V_bushing_enclosed
#   Path_V_hole_inverse
#   Path_V_machining_allowance
#   Path_V_passive_region_booster
#   Path_pin_bushing_enclosed
#   Path_pin_hole_inverse
#   Path_pin_machining_allowance
#   Path_fixture
#   Path_fixture_machining_allowance

from .ENVcc import CB_CAD_CONVERTER_PATHS as CCPaths

class CadConverterParameters:
    def __init__(self):
        self._plainParameters = {       # Protecting absolute paths ending to git origin
            "Path_LO_channels" : CCPaths["Path_LO_channels"],
            "Path_DS" : CCPaths["Path_DS"],
            "Path_machining" : CCPaths["Path_machining"],
            "Path_PR_bushing_enclosed" : CCPaths["Path_PR_bushing_enclosed"],
            "Path_PR_hole_inverse" : CCPaths["Path_PR_hole_inverse"], 
            "Path_PR_machining_allowance" : CCPaths["Path_PR_machining_allowance"],
            "Path_PR_passive_region_booster" : CCPaths["Path_PR_passive_region_booster"],
            "Path_PR_cyl_surf_bottom" : CCPaths["Path_PR_cyl_surf_bottom"],
            "Path_V_bushing_enclosed" : CCPaths["Path_V_bushing_enclosed"],
            "Path_V_hole_inverse" : CCPaths["Path_V_hole_inverse"],
            "Path_V_machining_allowance" : CCPaths["Path_V_machining_allowance"],
            "Path_V_passive_region_booster" : CCPaths["Path_V_passive_region_booster"],
            "Path_pin_bushing_enclosed" : CCPaths["Path_pin_bushing_enclosed"],
            "Path_pin_hole_inverse" : CCPaths["Path_pin_hole_inverse"],
            "Path_pin_machining_allowance" : CCPaths["Path_pin_machining_allowance"],
            "Path_fixture" : CCPaths["Path_fixture"],
            "Path_fixture_machining_allowance" : CCPaths["Path_fixture_machining_allowance"]
        }

    # Converts map to nTopology JSON input suitable format
    # NOTE:     Param1 is needed so that to create varying channel configuration.
    # TODO:     For future projects extend this function to be more flexible.
    # Param 1:  Absolute path to channel
    # Return:   list of maps [{<name>, <type>, <value>}, ...]
    def getBlockParamsJSON(self, channelPath):
        paramList = []
        for key in self._plainParameters:
            ntopConversion = {"name":key, "type":"text", "value":self._plainParameters[key]}
            if(key == "Path_LO_channels"):
                ntopConversion = {"name":key, "type":"text", "value":channelPath}
            paramList.append(ntopConversion)
        return paramList
    