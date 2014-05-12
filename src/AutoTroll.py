import sys
import praw
from CommentStore import comment_store
from AutoTrollThread import AutoTrollThread


def main(*args, **kwargs):
    """

    """
    try:
        trolls = create_auto_trolls(read_passwords_file('auto_troll.ini'))
    except Exception:
        print "parsing error with INI file"

class AutoTrollManager():

    def __init__(self):
        self.chumps = []
        self.trolls = []

    def create_auto_trolls(login_info):
        """
        creates n auto trolls
        this will take at least 2 * n seconds because reddit only allows one
        request every two seconds
        params:
            login_info, a list of username, password tuples
        returns:
            a list of AutoTrollThreds
        """
        return [troll for troll in map(
                                    lambda user,password: AutoTrollThread(
                                                            user,
                                                            password),
                                    login_info)]


    def read_passwords_file(password_file):
        """
        parses the passwords file to get login and passwords
        params:
            password_file (string) the path to the file
        returns:
            a list of tuples (login, password)

        """
        return [(line[0], line[1].strip('\n')) for line in
                map(lambda x: x.split('='), open(password_file, 'r'))]


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
