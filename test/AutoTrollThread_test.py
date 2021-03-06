# Auto Troll
# Author: Ace Levenberg (acelevenberg@gmail.com)
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <acelevenberg@gmail.com> wrote this file. As long as you retain this notice
# you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return
# ----------------------------------------------------------------------------

import unittest
import praw
import requests

from mock import patch
from AutoTrollThread import AutoTrollThread


class TestAutoTrollThread(unittest.TestCase):
    @patch('praw.Reddit')
    def setUp(self, mock_reddit):
        self.reddit = mock_reddit(user_agent='Auto Troll Testing v 0.1')
        self.login, self.password = get_login()
        self.troll = AutoTrollThread(self.login, self.password)

    def test_AutoTrollSend(self):
        thing = {}
        self.troll.send(thing)
        self.assertIs(thing, self.troll.input_queue.get())

    @patch('praw.objects.Comment')
    def test_AutoTrollPostComment(self, mock_comment):
        comment = mock_comment()
        self.troll._post("foo bar baz quz", comment)
        # Make sure that the reply was one of the calls in the mock comment
        call = str(mock_comment.mock_calls[1])
        self.assertGreater(len(call), 1)
        self.assertEquals('call().reply(\'foo bar baz quz\')', call)

    @patch('praw.objects.Submission')
    def test_AutoTrollPostSubmission(self, mock_submission):
        submission = mock_submission()
        self.troll._post("foo bar baz qux", submission)
        # Make sure that the reply was one of the calls in the mock submission
        call = str(mock_submission.mock_calls[1])
        self.assertGreater(len(call), 1)
        self.assertEquals('call().reply(\'foo bar baz qux\')', call)

    def test_AutoTrollPostNotCommentOrSubmission(self):
        # not sure how this is suppose to respond yet
        with self.assertRaises(TypeError):
            self.troll._post("foo bar", {})

    def test_getInsult(self):
        try:
            insult = self.troll.get_insult()
        except requests.exceptions.HTTPError as e:
            self.fail(msg=e.toString())
        self.assertIsInstance(insult, str)
        self.assertGreater(len(insult), 1)

    def test_timeout_time_minutes(self):
        minutes = self.troll.get_timeout_time("foo bar baz qux. 57 minutes.")
        self.assertEqual(minutes, 57*60)

    def test_timeout_time_seconds(self):
        seconds = self.troll.get_timeout_time("foo bar baz qux 30 seconds.")
        self.assertEqual(seconds, 60)


def get_login():
    with open('passwords.txt') as password:
        line = password.readline().split('=')
    login = line[0]
    password = line[1].strip('\n')
    return login, password

if __name__ == '__main__':
    unittest.main()
