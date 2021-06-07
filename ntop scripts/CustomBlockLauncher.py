import ENVIRONMENT
import AUTH
import colors

import os
import subprocess
import json

class CustomBlockLauncher:
    def __init__(self):
        pass
    # Makes a subprocess for nTopCL -command with parameters being:
    # Param 1: Dict including all the CB_main inputs with correct fields
    # Param 2: Path to save in.json -file
    # Param 3: Path to save out.json -file
    def startNtopCLsubprocess(self, blockInputs, pathJSONinput , pathJSONoutput):
        os.system("")

        #nTopCL arguments in a list
        Arguments = [ENVIRONMENT.PATH_NTOP_EXE]    # nTopCL path
        #Arguments.append(pythonPath[0])
        Arguments.append("-u")
        Arguments.append(AUTH.USER)
        Arguments.append("-w")
        Arguments.append(AUTH.PW)
        Arguments.append("-j")              # .json input argument
        Arguments.append(pathJSONinput)
        Arguments.append("-o")              # .json output argument
        Arguments.append(pathJSONoutput)
        Arguments.append(ENVIRONMENT.PATH_MAIN_CB)

        # # First phase comment:
        #   - Creating {channel_ID}_{material_ID}_input.json to correct case subfolder
        with open(pathJSONinput, 'w') as outfile:
            json.dump(blockInputs, outfile, indent=2)

        # Approach with timeout.
        # After 2 hours custom block is propably stuck
        try:
            subprocess.run(Arguments, timeout=7200)
        except subprocess.TimeoutExpired:
            print("nTopCL subprocess ran too long. Terminated.")
