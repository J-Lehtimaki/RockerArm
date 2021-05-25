from .testParameterHandler import FirstPhaseParameterHandlerTestCase as FPPHTC

import unittest

def suite():
    suite = unittest.TestSuite()
    suite.addTest(FPPHTC("test_parameter_handler"))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())