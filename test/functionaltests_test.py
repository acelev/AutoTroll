import unittest
import os
import sys
import praw
sys.path.insert(0, os.path.dirname("../src/AutoTroll.py"))
from AutoTrollThread import AutoTrollThread
from AutoTroll import read_passwords_file


class FunctionalTests(unittest.TestCase):
    TEST_SUB = 'AutoTroll'

    @unittest.skip
    def test_reply_to_comment(self):
        """
        logs in with the first user in passwords.txt
        gets a comment from /r/circlejerk and comments on it
        """
        login, password = read_passwords_file('passwords.txt')[0]
        auto_troll = AutoTrollThread(login, password)
        self.reddit = praw.Reddit(user_agent="AutoTroll Test")
        bot_circle_jerk = self.reddit.get_subreddit("botcirclejerk")
        comment = bot_circle_jerk.get_comments().next()
        auto_troll.start()
        auto_troll.send(comment)
        auto_troll.close()

    @unittest.skip
    def test_reply_to_submission(self):
        """
        logs in with the first two logins
        creates a submission with the first login
        (may require a captcha)
        responds to the post with the second login
        all done in /r/AutoTroll (test bed for AutoTroll private access only)
        """
        logins = read_passwords_file('passwords.txt')
        auto_troll = AutoTrollThread(logins[1][0], logins[1][1])
        self.reddit = praw.Reddit(user_agent='AutoTroll test')
        self.reddit.login(logins[0][0], logins[0][1])
        test_sub = self.reddit.get_subreddit(self.TEST_SUB)
        submission = self.reddit.submit(test_sub, 'Test', 'test')
        auto_troll.start()
        auto_troll.send(submission)
        auto_troll.close()

    def test_two_threads_reply_to_comments(self):
        """
        Logs in with the first two users in passwords.txt
        Gets all of the submissions from the first user
        responds to two submissions for each troll
        """
        logins = read_passwords_file('passwords.txt')
        auto_troll_1 = AutoTrollThread(logins[0][0], logins[0][1])
        auto_troll_2 = AutoTrollThread(logins[1][0], logins[1][1])
        self.reddit = praw.Reddit(user_agent='AutoTroll test')
        submissions = self.reddit.get_redditor(logins[0][0]).get_overview()
        auto_troll_1.start()
        auto_troll_2.start()
        auto_troll_1.send(next(submissions))
        auto_troll_1.send(next(submissions))
        auto_troll_2.send(next(submissions))
        auto_troll_2.send(next(submissions))
        print "all sent"
        auto_troll_1.close()
        auto_troll_2.close()

if __name__ == '__main__':
    unittest.main()
