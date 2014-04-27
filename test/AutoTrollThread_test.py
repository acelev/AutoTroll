import unittest
import praw
import sys
import requests

from AutoTrollThread import AutoTrollThread, praw_submission_wrapper

class TestAutoTrollThread(unittest.TestCase):
    def setUp(self):
        self.reddit = praw.Reddit(user_agent='Auto Troll Testing v 0.1')
        self.login, self.password = self.get_login() 
        self.troll = AutoTrollThread(self.login, self.password)

    def test_AutoTrollCreation(self):
        troll = AutoTrollThread(self.login, self.password)
        self.assertIsInstance(troll, AutoTrollThread)

    def test_AutoTrollBadCreation(self):
        self.assertRaises(praw.errors.InvalidUserPass, AutoTrollThread, self.login, 'notpassword' )
    def test_AutoTrollSend(self):
        thing = object
        self.troll.send(thing)
        self.assertIs(thing, self.troll.input_queue.get())
    def test_AutoTrollClose(self):
        self.troll.start()
        self.troll.close()
        self.assertIs(None, self.troll.input_queue.get()) 
    
    def test_AuoTrollPost(self):
        botcirclejerk = self.reddit.get_subreddit('botcirclejerk')
        random = botcirclejerk.get_random_submission()
        random_wrapped =  praw_submission_wrapper(random)
        try:
            comment = self.troll.post('foo bar baz qux', random_wrapped)
        except request.exceptions.HTTPError as e:
            self.fail(msg=e.toString())
    def get_login(self):
        with open('../src/passwords.txt') as password: 
            line = password.readline().split('=')
        login = line[0]
        password = line[1]  
        return login, password

if __name__ == '__main__':
    unittest.main()
