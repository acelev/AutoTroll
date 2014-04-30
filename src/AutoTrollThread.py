#Auto Troll
#Author: Ace Levenberg (acelevenberg@gmail.com)
#----------------------------------------------------------------------------
#"THE BEER-WARE LICENSE" (Revision 42):
#<acelevenberg@gmail.com> wrote this file. As long as you retain this notice you
#can do whatever you want with this stuff. If we meet some day, and you think
#this stuff is worth it, you can buy me a beer in return
#----------------------------------------------------------------------------

import threading
from Queue import Queue
import praw

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
    def __init__(self, username, password):
        """
        creates an instance of AutoTrollThread
        throws (login failure) if the login fails

        """
        self.input_queue = Queue()

        self.reddit = praw.Reddit(user_agent='AutoTroll v0.1')
        self.reddit.login(username, password)

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
            submisson = self.input_queue.get()
            if submisson is None:
                break
            insult = self.get_insult()
            self.post(insult, submission)
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

    def post(self, trolled_response, comment_to_troll):
        """
        posts a trolled_response to the comment provided
        params:
            trolled_response(string) the insult to respond
            comment_to_troll(PRAW post) to post to respond to
        returns:
            the comment object
        """
        reply_func = None
        if isinstance(comment_to_troll, praw.objects.Comment):
            reply_func = comment_to_troll.reply
        elif isinstance(comment_to_troll, praw.objects.Submission):
            reply_func = comment_to_troll.add_comment













