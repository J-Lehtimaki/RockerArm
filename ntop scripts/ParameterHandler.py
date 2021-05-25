from .CB_cad_converter import CadConverterParameters as CCparams
from .CB_manufacturing_data_exporter import ManFactDataParameters as MFDparams

import os

# Everything that is strictly related to forming feasible parameterset for
# the 1st phase sample generation goes here.
class FirstPhaseParameterHandler:
    def __init__(self):
        self._dynamicParamsLists = []       # List of lists of dicts [[{}], [{}], ..]
        self._constParams = []              # List of dicts [{}, {}, ...]

    # Creates channel shape based parameters and appends to dynamic variable list
    # Param1: [{"pathToChannel", "basename"}, ...]
    def parseAbsolutePathBasename(channelListDict):
        None

    
