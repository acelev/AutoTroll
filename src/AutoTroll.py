import sys
import praw
from CommentStore import comment_store
from AutoTrollThread import AutoTrollThread


def main(*args, **kwargs):
    """

    """

class AutoTrollManager():

    def __init__(self):
        self.chumps = []
        self.trolls = []

    def add_chump(self, chump):
        """
        Adds a chump to the list of chumps that are going to get trolled
        and starts the trolling process on the chump
        params:
            chump, the string containing the name of the chump
        """
        pass

    def remove_chump(self, chump):
        """
        removes a chump from the list of chumps
        params:
            chump, the name of the chump to remove
        """
        pass

    def remove_troll(self, username):
        """
        removes a troll from the army of trolls
        params:
            username, the name of the troll to remove
        """
        pass

    def add_troll(self, username, password):
        """
        Adds a new troll to the army of trolls
        params:
            username, the username name of the troll
            password, the password ofer the trol
        """
        try:
            self.trolls[username] = AutoTrollThread(username, password)
        except praw.errors.APIException as e:
            # log error
            print str(e)

    def add_trolls(self, logins):
        """
        adds n trolls
        params:
            logins, a list of tuples containing username, password pairs
        """
        pass

    def _create_auto_trolls(self, login_info):
        """
        creates n auto trolls
        this will take at least 2 * n seconds because reddit only allows one
        request every two seconds
        params:
            login_info, a list of username, password tuples
        returns:
            a list of AutoTrollThreds
        """
        # this fuinction is probably going to get removed
        return [troll for troll in map(
                                    lambda user, password: AutoTrollThread(user, password),
                                    login_info)]

    def get_sbumissions(self, chump):
        """
        gets the newest submissions of the user
        params:
            chump (string) the chump thats getting trolled
        returns:
            list of praw_comments and praw_submissions
        """
        pass

    def get_all_submissions(self):
        """
        gets all the submissions of all of the chumps
        input:
            none
        returns:
            a list of submissions and comments
        """

        submissions = []
        for chump in self.chumps:
            submisions.extend(self.get_sbumissions(chump)


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



def shell():
    """
    not sure what to call this....
    Acts as a repl for the AutoTroll
    """
    pass
