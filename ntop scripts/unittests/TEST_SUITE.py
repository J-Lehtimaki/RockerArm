from .testParameterHandler import FirstPhaseParameterHandlerTestCase as FPPHTC
from .testFileHandler import FirstPhaseFileHandlerTestCase as FPFHTC
from .testMaterialParameters import MaterialParametersTestCase as MPTC

import unittest

def suite():
    suite = unittest.TestSuite()
    suite.addTest(FPPHTC("test_parameter_handler"))
    suite.addTest(MPTC("test_material_parameters"))
    suite.addTest(FPFHTC("test_first_phase_filehandler"))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())