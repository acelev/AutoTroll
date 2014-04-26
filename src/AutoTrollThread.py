import threading
from Queue import Queue
import praw

class praw_submissions_wrapper():
    """
    wrapper to wrap submissions and comment objects together
    access to original object is available because im lazy
    usage:
        submission = praw_submissions_wrapper(comment)
        submission.respond("Spam Eggs")
        submissions.down_vote() 
    """ 
    UP = 0
    DOWN = 1
    def __init__(self,praw_content_object):
        """
        creates a comment object
        params:
            praw_content_object must be a submissions or comment object
        """
        pass
    
    def respond(self, comment):
        """
        responds to the submission
        params:
            comment(string) the response to the submissions 
        returns:
            a praw_submission_wrapper object containing the comment object returned
            by PRAW  
        """
        pass
    def vote(self, up_or_down):
        """ 
        votes up or down
        params:
            up_or_down(int) either UP or DOWN
        """
        pass 

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

    def send(self, comment_to_troll):
        """
        inserts a post/comment PRAW object into the thread queue
        params:
            comment_to_troll(praw_submissions_wrapper) the comment for this instance to troll 
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
        pass 
    def get_insult(self):
        """
        gets insult to troll chump with
        returns:
            (string) the insult
        """   
        pass
    def post(self, trolled_response, comment_to_troll):
        """
        posts a trolled_response to the comment provided
        params:
            trolled_response(string) the insult to respond
            comment_to_troll(PRAW comment/post object) to post to respond to 
        """
        pass
