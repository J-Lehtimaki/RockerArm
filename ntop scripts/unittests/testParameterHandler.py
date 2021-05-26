import unittest

from ParameterHandler import FirstPhaseParameterHandler as FPPH

class FirstPhaseParameterHandlerTestCase(unittest.TestCase):
    def setUp(self):
        self._FPPH = FPPH()
        self._fakeChannelDict = [
            {"absPath" : "C:\\my\\fake\\path\\1.stp", "basename" : "1"},
            {"absPath" : "C:\\my\\fake\\path\\2.stp", "basename" : "2"},
            {"absPath" : "C:\\my\\fake\\path\\3.stp", "basename" : "3"},
            {"absPath" : "C:\\my\\fake\\path\\4.stp", "basename" : "4"},
            {"absPath" : "C:\\my\\fake\\path\\5.stp", "basename" : "5"},
            {"absPath" : "C:\\my\\fake\\path\\6.stp", "basename" : "6"},
            {"absPath" : "C:\\my\\fake\\path\\7.stp", "basename" : "7"},
            {"absPath" : "C:\\my\\fake\\path\\8.stp", "basename" : "8"}
        ]

    def testCadConverterParameterBuilder(self):
        a = self._FPPH.createCadConverterParameters(self._fakeChannelDict)
        self.assertTrue(len(self._FPPH.getDynamicParamsLists()["CadConverterParams"]) == 8)
        self.assertTrue(
            self._FPPH.getDynamicParamsLists()["CadConverterParams"][7][0]["value"] ==
            "C:\\my\\fake\\path\\8.stp"
        )

