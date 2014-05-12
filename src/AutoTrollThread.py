#Auto Troll
#Author: Ace Levenberg (acelevenberg@gmail.com)
#----------------------------------------------------------------------------
#"THE BEER-WARE LICENSE" (Revision 42):
#<acelevenberg@gmail.com> wrote this file. As long as you retain this notice you
#can do whatever you want with this stuff. If we meet some day, and you think
#this stuff is worth it, you can buy me a beer in return
#----------------------------------------------------------------------------

import threading
import urllib2
import re
import requests
import logging
import time
from Queue import Queue
import praw

from CommentStore import comment_store
class AutoTrollThread(threading.Thread):

    """
    The actual AutoTroll
    each AutoTrollThread has its own troll login and
    praw reddit object
    usage:
    auto_troll = AutoTrollThread('username', 'password')
    auto_troll.send(comment_to_troll)
    auto_troll.run()
    """
    INSULT_RETRIES = 1
    POST_RETRIES = 1
    def __init__(self, username, password):
        """
        creates an instance of AutoTrollThread
        throws (login failure) if the login fails

        """
        threading.Thread.__init__(self)
        self.daemon = True
        self.input_queue = Queue()
        self.reddit = praw.Reddit(user_agent='AutoTroll v0.1 user = ' + username)
        self.reddit.login(username, password)
        self.username = username
        self.comment_store = comment_store()

    def send(self, comment_to_troll):
        """
        inserts a post/comment PRAW object into the thread queue
        params:
            comment_to_troll(PRAW POST or COMMENT) the comment for this instance to troll
        """
        self.input_queue.put(comment_to_troll)
    def close(self):
        """
        closes the thread
        """
        self.input_queue.put(None)
        self.input_queue.join()
    def run(self):
        """
        starts the thread
        """
        while True:
            submission = self.input_queue.get()
            if submission is None:
                break
            self.post(submission)
            self.input_queue.task_done()
        self.input_queue.task_done()
        return

    def get_insult(self):
        """
        gets insult to troll chump with
        Insultgenerator.org is awesome!
        returns:
            (string) the insult
        """
        #"parses" the html, I need to find one tag that is at the top level
        #this is just how insultgenerator works I know its dirty
        response = urllib2.urlopen('http://insultgenerator.org')
        insult = ""
        for line in response:
            match_object = re.match(r'<TR align=center><TD>(.*)', line)
            if match_object is not None:
                insult = match_object.group(1)
                break
        response.close()
        return insult

    def post(self, comment_to_troll):
        i = self.INSULT_RETRIES + 1
        insult = None
        while i > 0:
            try:
                insult = self.get_insult()
            except requests.HTTPError as e:
                # Log the error and try again
                # log error
                i -= 1
                continue
            break
        if insult is not None:
            response = None
            i = self.POST_RETRIES + 1
            while i > 0:
                try:
                    comment_to_troll.downvote()
                except praw.errors.APIException as e:
                    # log error
                    pass
                try:
                    response = self._post(insult, comment_to_troll)
                except praw.errors.RateLimitExceeded as e:
                    # Log error
                    time.sleep(600)
                    continue
                except praw.errors.APIException as e:
                    # log error
                    pass
                break
            if response is None:
                # Log the error
                pass
            else:
                self.comment_store.store_comment(self.username,
                                                 comment_to_troll.author,
                                                 comment_to_troll.id,
                                                 response.id,
                                                 response.created)

    def _get_reply_func(self, comment_to_troll):
        reply_func = None
        if hasattr(comment_to_troll, 'reply'):
            reply_func = comment_to_troll.reply
        elif hasattr(comment_to_troll, 'add_comment'):
            reply_func = comment_to_troll.add_comment
        return reply_func

    def _post(self, response, comment):
            comment.reddit_session = self.reddit
            reply_func = self._get_reply_func(comment)
            return reply_func(response)











