import optarg
import sys
import praw
from CommentStore import comment_store
from AutoTrollThread import AutoTrollThread


def main(*args, **kwargs):
    """
     
    """ 

def create_auto_trolls(n):
    """
    creates n auto trolls 
    this will take at least 2 * n seconds because reddit only allows one
    request every two seconds
    params:
        n, the number of auto trolls to create
    returns:
        a list of AutoTrollThreds
    """
    pass

def read_passwords_file(password_file):
    """
    parses the passwords file to get login and passwords
    params:
        password_file (string) the path to the file
    returns:
        a list of tuples (login, password)
    
    """
    pass

def get_sbumissions(chump):
    """
    gets the newest submissions of the user
    params:
        chump (PRAW redditor object) the chump thats getting trolled
    returns:
        lists of praw_submission_wrappers
    """

def shell():
    """
    not sure what to call this....
    Acts as a repl for the AutoTroll
    """ 
    pass
