#! /usr/bin/env python


import os
import sys
import unittest


def main():

    project_path = os.path.split(os.path.dirname(__file__))
    sys.path.append(project_path[0])
    test_loader = unittest.TestLoader()
    tests = test_loader.discover("tests", "*tests.py")
    result = unittest.TextTestRunner().run(tests)

    if not result.wasSuccessful():
        sys.exit(1)


if __name__ == '__main__':
    main()
