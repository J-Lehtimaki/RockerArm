from ntpath import join
import CBP
import sys
import os

# Some fake variables for testing purposes
channel_id = "myChannelID"
material_id = "316L-0410"
pathToMyChannel = "----pathToMyChannel----"
materials = ["IN718", "316L"]
ch_paths = [
    "C:\\some\\fake\\path\\1.stp",
    "C:\\some\\fake\\path\\22.stp",
    "C:\\some\\fake\\path\\333.stp",
    "C:\\some\\fake\\path\\4444.stp",
    "C:\\some\\fake\\path\\55555.stp",
    "C:\\some\\fake\\path\\666666.stp",
]

# Creates inputs for topology optimization
def joinedParameterList(ch_id, m_id, chPath):
    material = CBP.getMaterialParameterJSON(m_id)
    cadBodies = CBP.getCADconverterParameterListJSON(chPath)
    topPars = CBP.getTopOptParameterListJSON(ch_id, m_id)
    return [*material, *cadBodies, *topPars]

# Prints each block parameters separately
def one():
    # List 1
    material = CBP.getMaterialParameterJSON(material_id)
    for i in material:
        print(i)

    print("\nBreak\n")

    # List 2
    cadBodies = CBP.getCADconverterParameterListJSON(pathToMyChannel)
    for i in cadBodies:
        print(i)

    print("\nBreak\n")

    # List 3
    topPars = CBP.getTopOptParameterListJSON(channel_id, material_id)
    for i in topPars:
        print(i)

# Prints joined parameters that can be dumped to JSON
def two():
    material = CBP.getMaterialParameterJSON(material_id)
    cadBodies = CBP.getCADconverterParameterListJSON(pathToMyChannel)
    topPars = CBP.getTopOptParameterListJSON(channel_id, material_id)
    # Merge lists to create output for INPUT.JSON ntopology
    joinedList = [*material, *cadBodies, *topPars]
    for i in joinedList:
        print(i)

def three():
    for m in materials:
        pars = joinedParameterList(channel_id,m,pathToMyChannel)
        for par in pars:
            print(par)
        print("\nBREAK\n")


# Parsing ID number from channel path, returing tuple
def four():
    retVal = []
    for p in ch_paths:
        path = p
        id = p.split('\\')[-1].split('.')[0]
        retVal.append({"p":path,"channel_id":id})
    for pair in retVal:
        s = f'Path is: {pair["p"]} /**/ Channel ID is: {pair["channel_id"]}'
        print(s)

if(sys.argv[1] == str(1)): one()
if(sys.argv[1] == str(2)): two()
if(sys.argv[1] == str(3)): three()
if(sys.argv[1] == str(4)): four()

