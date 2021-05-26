import unittest

from FileHandler import FirstPhaseFileHandler as FPFH

class FirstPhaseFileHandlerTestCase(unittest.TestCase):
    def setUp(self):
        self.FileHandler = FPFH()
        self.FileHandler.createFileSystem()

    def fileHandlerTestPrint(self, msg):
        print(f"\nFILEHANDLER TEST - {msg}\n")

    def testGetVerMajorDict(self):
        idPathDict = self.FileHandler.getVerMajorDict()
        self.assertEqual(36, len(idPathDict))

        self.fileHandlerTestPrint("idPathDict")
        for key in idPathDict:
            print(key)

