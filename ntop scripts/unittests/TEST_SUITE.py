from .testParameterHandler import FirstPhaseParameterHandlerTestCase as FPPHTC

from .testMaterialParameters import MaterialParametersTestCase as MPTC

import unittest

def suite():
    suite = unittest.TestSuite()
    suite.addTest(FPPHTC("test_parameter_handler"))
    suite.addTest(MPTC("test_material_parameters"))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())