import sys
import os
import unittest


def print_results(results):
    for failure in results.failures:
        test, fail = failure
        print test
        print "FAILED :"
        print fail
        print "_____________"
    for error in results.errors:
        print error
        print" __________________"

sys.path.insert(0, os.path.dirname("../src/AutoTroll.py"))
results = unittest.TestResult()
unittest.TestLoader().loadTestsFromName("AutoTrollThread_test").run(results)
print_results(results)
results = unittest.TestResult()
unittest.TestLoader().loadTestsFromName("CommentStore_test").run(results)
print_results(results)
