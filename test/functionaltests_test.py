import unittest
import os
import sys
import praw
sys.path.insert(0, os.path.dirname("../src/AutoTroll.py"))
from AutoTrollThread import AutoTrollThread
from AutoTrollThread_test import get_login


class FunctionalTests(unittest.TestCase):
    def test_create_thread_post_twice(self):
        login, password = get_login()
        password = password.strip('\n')
        auto_troll = AutoTrollThread(login, password)
        self.reddit = praw.Reddit(user_agent="AutoTroll Test")
        bot_circle_jerk = self.reddit.get_subreddit("botcirclejerk")
        random_submission = bot_circle_jerk.get_random_submission()
        comment = bot_circle_jerk.get_comments().next()
        auto_troll.start()
        auto_troll.send(random_submission)
        auto_troll.send(comment)
        auto_troll.close()

if __name__ == '__main__':
    unittest.main()
