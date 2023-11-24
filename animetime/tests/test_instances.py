import unittest
from animetime.common.instances import *

class testInstances(unittest.TestCase):
    def test_instance_exist(self):
        test_index = {"TESTINSTANCE": ""}
        test_instance_id = "TESTINSTANCE"
        self.assertTrue(instance_exist(test_instance_id, test_index, False, ""))
        self.assertFalse(instance_exist("NONE", test_index, False, ""))

    def test_delete_instance(self):
        test_index = {"TESTINSTANCE1": "", "TESTINSTANCE2": ""}
        delete_instance(test_index)
        self.assertEqual(test_index, {})
        test_index = {"TESTINSTANCE1": "", "TESTINSTANCE2": ""}
        delete_instance(test_index, ["TESTINSTANCE1"])
        self.assertEqual(test_index, {"TESTINSTANCE2": ""})

    def test_select_all_instances(self):
        test_index = {"TESTINSTANCE1" :"", "TESTINSTANCE2": ""}
        self.assertEqual(select_all_instances(test_index), list(test_index.keys()))
        self.assertEqual(select_all_instances(test_index, ["TESTINSTANCE1"]), ["TESTINSTANCE1"])