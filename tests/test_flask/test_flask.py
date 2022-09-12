#!/usr/bin/python3
"""Test api Flask
"""
from api.v1 import app
import inspect
import pep8
import unittest


class TestAppDocs(unittest.TestCase):
    """test Flask docs"""

    all_funcs = inspect.getmembers(app, inspect.isfunction)

    @classmethod

    def test_doc_file(self):
        """... docu for the file"""
        actual = app.__doc__
        self.assertIsNotNone(actual)

    def test_all_function_docs(self):
        """... ALL DOCS for all functions in db_storage file"""
        all_functions = TestAppDocs.all_funcs
        for function in all_functions:
            self.assertIsNotNone(function[1].__doc__)


if __name__ == '__main__':
    unittest.main
