import sys
import os
import unittest 

sys.path.insert(0, os.path.dirname("../src/AutoTroll.py"))
result = unittest.TestResult()
unittest.TestLoader().loadTestsFromName("AutoTrollThread_test").run(result)
for failure in result.failures:
    test, fail = failure
    print test
    print "FAILED REASON:"
    print fail 
    print "_____________"
for error in result.errors:
    print error
    print" __________________"
