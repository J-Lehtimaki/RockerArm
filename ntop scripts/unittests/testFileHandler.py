import unittest

from FileHandler import FirstPhaseFileHandler as FPFH

class FirstPhaseFileHandlerTestCase(unittest.TestCase):
    def setUp(self):
        self.FileHandler = FPFH()

    def testNumberOfMajorFolders(self):
        self.FileHandler.createFileSystem()
