# -*- coding: utf-8 -*-
#
# This software is licensed under the same terms and conditions as
# Python itself. See the file LICENSE.txt for more details.
#
# It is based on Python's Lib/test/test_winreg.py.
#
# Test the Cygwin specific cygwinreg3 module.

from cygwinreg3 import *
from cygwinreg3.constants import *
import errno
import os
import unittest

ut = unittest.TestCase()
test_key_name = "SOFTWARE\\Python Registry Test Key - Delete Me"

test_data = [
    ("Int Value",    45,                                 REG_DWORD),
    ("Long Value",   2**45,                              REG_QWORD),
    ("String Val",   "A string value",                   REG_SZ),
    ("StringExpand", "The path is %path%",               REG_EXPAND_SZ),
    ("Multi-string", ["Lots", "of", "string", "values"], REG_MULTI_SZ),
    ("Raw Data",     b"binary\0data",                    REG_BINARY),
    ("Big String",   "x"*(2**14-1),                      REG_SZ),
    ("Big Binary",   b"x"*(2**14),                       REG_BINARY),
    ]


def WriteTestData(root_key):
    # Set the default value for this key.
    SetValue(root_key, test_key_name, REG_SZ, "Default value")
    key = CreateKey(root_key, test_key_name)
    # Create a sub-key
    sub_key = CreateKey(key, "sub_key")
    # Give the sub-key some named values

    for value_name, value_data, value_type in test_data:
        SetValueEx(sub_key, value_name, 0, value_type, value_data)

    # Check we wrote as many items as we thought.
    nkeys, nvalues, since_mod = QueryInfoKey(key)
    ut.assertEqual(nkeys, 1, "Not the correct number of sub keys")
    ut.assertEqual(nvalues, 1, "Not the correct number of values")
    nkeys, nvalues, since_mod = QueryInfoKey(sub_key)
    ut.assertEqual(nkeys, 0, "Not the correct number of sub keys")
    ut.assertEqual(nvalues, len(test_data), "Not the correct number of values")
    # Check that FlushKey doesn't throw exceptions
    FlushKey(sub_key)
    # Close this key this way...
    # (but before we do, copy the key as an integer - this allows
    # us to test that the key really gets closed).
    int_sub_key = int(sub_key)
    CloseKey(sub_key)
    try:
        QueryInfoKey(int_sub_key)
        raise RuntimeError(
            "It appears the CloseKey() function does not close the actual key!")
    except EnvironmentError:
        pass
    # ... and close that key that way :-)
    int_key = int(key)
    key.Close()
    try:
        QueryInfoKey(int_key)
        raise RuntimeError(
            "It appears the key.Close() function does not close the actual key!")
    except EnvironmentError:
        pass


def remove(filename):
    try:
        os.remove(filename)
    except OSError as e:
        if e.errno == errno.ENOENT:
            pass                    # Ignore non-existant removal


def BackupTestData(root_key):
    sub_key = OpenKey(OpenKey(root_key, test_key_name), "sub_key")
    # Check that SaveKey and LoadKey don't throw exceptions
    tempfile = os.environ["LOCALAPPDATA"] + r'\Temp\test_reg'
    remove(tempfile)
    try:
        SaveKey(sub_key, tempfile)
        try:
            LoadKey(root_key, "sub_key", tempfile)
        except WindowsError as e:
            if e.winerror == 5:
                pass                # Needs SE_RESTORE_PRIVILEGE
    finally:
        remove(tempfile)


def ReadTestData(root_key):
    # Check we can get default value for this key.
    val = QueryValue(root_key, test_key_name)
    ut.assertEqual(val, "Default value",
                   "Registry didn't give back the correct value")

    key = OpenKey(root_key, test_key_name)
    # Read the sub-keys
    sub_key = OpenKey(key, "sub_key")
    # Check I can enumerate over the values.
    index = 0
    while 1:
        try:
            data = EnumValue(sub_key, index)
        except EnvironmentError:
            break
        ut.assertIn(data, test_data, "Didn't read back the correct test data")
        index = index + 1
    ut.assertEqual(index, len(test_data),
                   "Didn't read the correct number of items")
    # Check I can directly access each item
    for value_name, value_data, value_type in test_data:
        read_val, read_typ = QueryValueEx(sub_key, value_name)
        ut.assertEqual(read_val, value_data,
                       "Could not directly read the value")
        ut.assertEqual(read_typ, value_type,
                       "Could not directly read the value")
    sub_key.Close()
    # Enumerate our main key.
    read_val = EnumKey(key, 0)
    ut.assertEqual(read_val, "sub_key", "Read subkey value wrong")
    try:
        EnumKey(key, 1)
        ut.fail("Was able to get a second key when I only have one!")
    except EnvironmentError:
        pass

    key.Close()


def DeleteTestData(root_key):
    key = OpenKey(root_key, test_key_name, 0, KEY_ALL_ACCESS)
    sub_key = OpenKey(key, "sub_key", 0, KEY_ALL_ACCESS)
    # It is not necessary to delete the values before deleting
    # the key (although subkeys must not exist).  We delete them
    # manually just to prove we can :-)
    for value_name, value_data, value_type in test_data:
        DeleteValue(sub_key, value_name)

    nkeys, nvalues, since_mod = QueryInfoKey(sub_key)
    ut.assertEqual(nkeys + nvalues, 0, "subkey not empty before delete")
    sub_key.Close()
    DeleteKey(key, "sub_key")

    try:
        # Shouldnt be able to delete it twice!
        DeleteKey(key, "sub_key")
        ut.fail("Deleting the key twice succeeded")
    except EnvironmentError:
        pass
    key.Close()
    DeleteKey(root_key, test_key_name)
    # Opening should now fail!
    try:
        key = OpenKey(root_key, test_key_name)
        ut.fail("Could open the non-existent key")
    except WindowsError:  # Use this error name this time
        pass


def TestAll(root_key):
    WriteTestData(root_key)
    BackupTestData(root_key)
    ReadTestData(root_key)
    DeleteTestData(root_key)
    ConnectRegistry(None, root_key).Close()


test = unittest.FunctionTestCase(lambda: TestAll(HKEY_CURRENT_USER))
unittest.TextTestRunner().run(test)
