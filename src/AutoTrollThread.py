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

    def send(self, comment_to_troll):
        """
        params:
            comment_to_troll(PRAW Comment Object) the comment for this instance to troll 
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
    
