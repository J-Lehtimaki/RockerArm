import unittest

from CB_material.MaterialParameters import MaterialParameters as MP

class MaterialParametersTestCase(unittest.TestCase):
    def setUp(self):
        self._MP = MP()

    def materialTestPrint(self, msg):
        print(f"\nMATERIAL TESTS - {msg}\n")

    def testIN718(self):
        inconel = self._MP.getMaterialByID("IN718")
        self.assertTrue(len(inconel) == 3)
        self.assertTrue(inconel[0]["name"] == "youngs_modulus")
        self.assertTrue(inconel[0]["units"] == "Pa")
        self.assertTrue(inconel[0]["values"] == 205000000000)

        self.assertTrue(inconel[1]["name"] == "poissons_ratio")
        self.assertTrue(inconel[1]["type"] == "scalar")
        self.assertTrue(inconel[1]["values"] == 0.284)

        self.assertTrue(inconel[2]["name"] == "density")
        self.assertTrue(inconel[2]["units"] == "g/cm^3")
        self.assertTrue(inconel[2]["values"] == 8.19)

    def testGetAllMaterials(self):
        t = self._MP.getAllBlockParamsJSON()

        # Excpect [[{},{},{}, ...], [], ...]
        # Currently there are only 2 materials
        self.assertTrue(len(t) == 2)

        # Test access inconell
        self.assertTrue(t[0][0]["name"] == "youngs_modulus")
        self.assertTrue(t[0][0]["units"] == "Pa")
        self.assertTrue(t[0][0]["values"] == 205000000000)

        self.assertTrue(t[0][1]["name"] == "poissons_ratio")
        self.assertTrue(t[0][1]["type"] == "scalar")
        self.assertTrue(t[0][1]["values"] == 0.284)

        self.assertTrue(t[0][2]["name"] == "density")
        self.assertTrue(t[0][2]["units"] == "g/cm^3")
        self.assertTrue(t[0][2]["values"] == 8.19)

    def testGetMaterialsByID(self):
        t = self._MP.getMaterialsByID(["IN718", "316L"])

        # Excpect [[{},{},{}, ...], [], ...]
        # Currently there are only 2 materials
        self.assertTrue(len(t) == 2)

        # Test access inconell
        self.assertTrue(t[0][0]["name"] == "youngs_modulus")
        self.assertTrue(t[0][0]["units"] == "Pa")
        self.assertTrue(t[0][0]["values"] == 205000000000)

        self.assertTrue(t[0][1]["name"] == "poissons_ratio")
        self.assertTrue(t[0][1]["type"] == "scalar")
        self.assertTrue(t[0][1]["values"] == 0.284)

        self.assertTrue(t[0][2]["name"] == "density")
        self.assertTrue(t[0][2]["units"] == "g/cm^3")
        self.assertTrue(t[0][2]["values"] == 8.19)

    def testPrint(self):
        t = self._MP.getMaterialsByID(["IN718", "316L"])
        self.materialTestPrint("Looping the getMaterialsByID")

        self.materialTestPrint("316L")
        for i in t[1]:
            print(i)
        self.materialTestPrint("Inconel")
        for i in t[0]:
            print(i)

        b = self._MP.getAllBlockParamsJSON()
        self.materialTestPrint("Looping the getAllBlockParamsJSON")
        for i in b[1]:
            print(i)
        self.materialTestPrint("Inconel")
        for i in b[0]:
            print(i)

