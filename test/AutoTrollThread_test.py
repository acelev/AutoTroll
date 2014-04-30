#Auto Troll
#Author: Ace Levenberg (acelevenberg@gmail.com)
#----------------------------------------------------------------------------
#"THE BEER-WARE LICENSE" (Revision 42):
#<acelevenberg@gmail.com> wrote this file. As long as you retain this notice you
#can do whatever you want with this stuff. If we meet some day, and you think
#this stuff is worth it, you can buy me a beer in return
#----------------------------------------------------------------------------

import unittest
import praw
import sys
import requests

from AutoTrollThread import AutoTrollThread


class TestAutoTrollThread(unittest.TestCase):

    def setUp(self):
        self.reddit = praw.Reddit(user_agent='Auto Troll Testing v 0.1')
        self.login, self.password = self.get_login()
        self.troll = AutoTrollThread(self.login, self.password)

    def test_AutoTrollCreation(self):
        troll = AutoTrollThread(self.login, self.password)
        self.assertIsInstance(troll, AutoTrollThread)

    def test_AutoTrollBadCreation(self):
        self.assertRaises(praw.errors.InvalidUserPass,
                          AutoTrollThread,
                          self.login,
                          'notpassword')

    def test_AutoTrollSend(self):
        thing = {}
        self.troll.send(thing)
        self.assertIs(thing, self.troll.input_queue.get())

    def test_AutoTrollPost(self):
        botcirclejerk = self.reddit.get_subreddit('botcirclejerk')
        random = botcirclejerk.get_random_submission()
        try:
            #if a comment is returned I know it was posted due to PRAW
            comment = self.troll.post('foo bar baz qux', random)
            self.assertIsInstance(comment, praw.objects.Comment)
        except requests.exceptions.HTTPError as e:
            self.fail(msg=e.toString())

    def test_AutoTrollPostNotCommentOrSubmission(self):
        self.troll.post("foo bar", {})
        #not sure how this is suppose to respond yet


    def test_AutoTrollPostTwice(self):
        #unsure of proper response at the moment
        botcirclejerk =  self.reddit.get_subreddit('botcirclejerk')
        random = botcirclejerk.get_random_submission()
        try:
            self.troll.post('spam eggs', random)
        except requests.exceptions.HTTPError as e:
            self.fail(msg=e.toString())

    def test_getInsult(self):
        try:
            insult = self.troll.get_insult()
        except requests.exceptions.HTTPError as e:
            self.fail(msg=e.toString())
        self.assertIsInstance(insult, str)
        self.assertGreater(len(insult), 1)

    def get_login(self):
        with open('passwords.txt') as password:
            line = password.readline().split('=')
        login = line[0]
        password = line[1]
        return login, password

if __name__ == '__main__':
    unittest.main()
