import os
import subprocess
import json
import sys
from pathlib import Path
import ctypes, sys
import ENVIRONMENT
import AUTH


class TopologyCaller:

    def __init__(self):
        pass
    # Makes a subprocess for nTopCL -command with parameters being:
    # Param 1: Path to .stp -file lubrication oil channels
    # Param 2: Path where nTopology output .x_t -file will be saved
    # Param 3: Path
    # Param 4: Path
    def subProcessRockerArm(self, inputStepLOchannel, outputParasolid, inputfileJSON, outputfileJSON):
        os.system("")
        #Assuming this script, ntop file, and json files will be in the same folder
        exePath = ENVIRONMENT.PATH_NTOP_EXE  #nTopCL path
        nTopFilePath = ENVIRONMENT.PATH_CB   #nTop notebook file name

        print("INPUTS",
            inputStepLOchannel, inputStepLOchannel[0], "\n",
            outputParasolid, outputParasolid[0], "\n",
            inputfileJSON, inputfileJSON[0], "\n",
            outputParasolid, outputParasolid[0], "\n")
        Input_File_Name = str(Path(inputfileJSON[0]))
        Output_File_Name = str(Path(outputfileJSON))    #JSON output file name to be saved as

        Inputs_JSON = {
            "inputs": [
                {"name": "PATH_input_channels", "type": "text", "value": str(Path(inputStepLOchannel[0]))},
                {"name": "PATH_channel_export_parasolid", "type": "text", "value": str(Path(outputParasolid[0]))}
            ]
        }

        #nTopCL arguments in a list
        Arguments = [exePath]               #nTopCL path
        #Arguments.append(pythonPath[0])
        Arguments.append("-u")
        Arguments.append(AUTH.USER)
        Arguments.append("-w")
        Arguments.append(AUTH.PW)
        Arguments.append("-j")              #json input argument
        Arguments.append(Input_File_Name)   #json path
        Arguments.append("-o")              #output argument
        Arguments.append(Output_File_Name)  #output json path
        Arguments.append(nTopFilePath)      #.ntop notebook file path

        
        print('{YELLOW}{inputfileJSON}{RESET}'.format(YELLOW=YELLOW, inputfileJSON=inputfileJSON, RESET=RESET))
        print("FROM nTopCall3.py:  ----------> ", inputfileJSON[0])

        #Creating in.json file
        with open(Input_File_Name, 'w') as outfile:
            json.dump(Inputs_JSON, outfile, indent=4)

        print('ARGUMENTS BEFORE SP CALL ----------->', Arguments)

        sp = subprocess.Popen(Arguments, shell=True ,stdout = subprocess.PIPE, stderr= subprocess.PIPE)
        sp.wait()
        output, error = sp.communicate()

        print(f'{YELLOW} {output} {RESET}')

        if (error != ""):
            print('{s}ERROR in subprocess! ---------> {e} {end}'.
                format(s=RED, e=error, end=RESET))
            print(error)
