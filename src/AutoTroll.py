import sys
import praw
from CommentStore import comment_store


def main(*args, **kwargs):
    """

    """
    pass


class ChumpManager():
    """
    Keeps track of all the chumps we are trolling
    """
    def __init__(self):
        self.chumps = []
        self.reddit = praw.Reddit(user_agent="AutoTroll v0.1")
        self.commnet_store = comment_store()
        self.removed_chumps = set()

    def delete_chump(self, chump):
        """
        removes the chump from the list and from the comment store
        params:
            chump(string), the chump to remove
        """
        # If we remove the chump from the chumps then we have to be carefull
        # when we generate the submissions objects, if we have something like
        # ChumpManager.get_all_submissions() that returns a generator object
        # that walks through the submissions in each chump we could potentially
        # delete that chump while it is in use by the generator...
        self.commnet_store.remove_chump(chump)
        self.removed_chumps.add(chump)

    def add_chump(self, chump):
        """
        Adds a chump to the list of chumps that are going to get trolled
        and starts the trolling process on the chump
        params:
            chump, the string containing the name of the chump
        """
        if chump not in self.chumps:
            self.chumps[chump] = self.get_sbumissions(chump)

    def get_sbumissions(self, chump):
        """
        gets the newest submissions of the chump
        params:
            chump (string) the chump thats getting trolled
        returns:
            generator object of praw_comments and praw_submissions
        """
        last_trolled_comment = self.comment_store.get_last_trolled_comment(chump)
        try:
            chump_account = self.reddit.get_redditor(chump)
            untrolled_submissions = chump_account.get_overview(
                                                    params={'after': last_trolled_comment})
        except praw.errors.APIException as e:
            # log error
            print str(e)
        return untrolled_submissions

    def get_all_submissions(self):
        """
        gets all the submissions of all of the chumps
        input:
            none
        returns:
            a list of generator objects containing comments and submissions
        """

        submissions = []
        for chump in self.chumps:
            submissions.add(self.get_sbumissions(chump))
        return submissions

    def read_chumps_from_file(self):
        """
        reads the chumps from the cached csv file
        """
        for chump in self.comment_store.get_stored_chumps():
            self.add_chump(chump)


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
