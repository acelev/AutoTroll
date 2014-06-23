import unittest
import os
import sys
import praw
sys.path.insert(0, os.path.dirname("../src/AutoTroll.py"))
from mock import patch
from AutoTrollThread import AutoTrollThread
from AutoTroll import read_passwords_file
from AutoTrollManager import AutoTrollManager

class TestTrollManager(unittest.TestCase):
    def setUp(self):
        self.troll_manager = AutoTrollManager()

    @patch('AutoTrollThread.AutoTrollThread')
    def test_manager_remove_troll(self, mock_troll):
        self.troll_manager.trolls['Test'] = mock_troll('spam', 'eggs')
        self.troll_manager.remove_troll('Test')
        self.assertNotIn('Test', self.troll_manager.trolls)
        self.assertIn('Test', self.troll_manager._removed_trolls)

    # still missing the case that the troll are over the threshold
    @patch('AutoTrollThread.AutoTrollThread')
    def test_find_next_troll(self, mock_troll):
        self.troll_manager.trolls['spam'] = mock_troll('spam' , 'eggs')
        troll = self.troll_manager._find_next_troll().next()
        self.assertIs(troll, self.troll_manager.trolls['spam'])
        self.troll_manager.trolls['eggs'] = mock_troll('foo' , 'bar')
        troll2 = self.troll_manager._find_next_troll().next()
        # tests to see if the generator actually returns the object after the
        # initial loop has been called
        self.assertIs(troll2, self.troll_manager.trolls['eggs'])
        self.assertRaises(self.troll_manager._find_next_troll().next())



if __name__ == '__main__':
    unittest.main()
