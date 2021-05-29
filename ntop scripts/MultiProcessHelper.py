# Author: Janne Lehtimäki
# e-mail: janne.lehtimaki@etteplan.com
# Company: Etteplan Finland Oy

# Class for helper functions when passing parameters for processes
class MultiProcessHelper:
    def __init__(self):
        pass

    # Returns [][] list of lists, amount being n
    def splitInputToEqualLists(self, originalList, n):
        copyInputs = originalList
        result = []     # append sliced copyinputs here
        subsetSize = len(copyInputs)//n
        # Process files that are in the range of subsetSize
        for i in range(0,n):
            result.append(copyInputs[0:subsetSize])
            del copyInputs[0:subsetSize]
        # Process remainder files
        tracker = 0     # Tracker for dividing equally to different processes
        for f in copyInputs:
            result[tracker].append(f)
            tracker += 1
        return result
