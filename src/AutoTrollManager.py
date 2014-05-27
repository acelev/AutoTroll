import praw
from AutoTrollThread import AutoTrollThread


class AutoTrollManager():

    def __init__(self, max_submission_threshold=-1):
        self.trolls = dict()
        self._removed_trolls = dict()
        self._troll_generator = self._next_troll()
        self.submission_threshhold = max_submission_threshold
        self._next_troll = None

    def remove_troll(self, username):
        """
        removes a troll from the army of trolls if the troll has no submissions
        left. If there are remianing submissions the Troll will respond to them
        before it is removed
        params:
            username, the name of the troll to remove
        """
        # moves the troll to the removed trolls dictionary
        self._removed_trolls[username] = self.trolls.pop(username)
        # close the thread
        self._removed_trolls[username].close()

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
        for login, password in logins:
            self.add_troll(login, password)

    def get_num_trolls(self):
        return len(self.trolls)

    def check_trolls_available(self):
        """
        checks to see if there are trolls available, this is only used
        if you have set max_submissions_threshold
        it will always return True if you have not set a threshold
        returns:
            bool, True if there are trolls available false if there are not
        """
        # set the next troll so we do not cycle through the list again
        self._next_troll = self._get_next_troll()
        return self._next_troll is not None

    def troll_submission(self, submission):
        """
        sends a submission to the Troll with the least load on it
        input:
            submission(praw submission object) submission to troll
        """
        # if we have checked for available trolls then we do not need to cycle
        # through the list again
        if self._next_troll is not None:
            self._next_troll.send(submission)
            # we have used the troll and need to retrieve another one next time
            self._next_troll = None
        else:
            next_troll = self._get_next_troll()
            if next_troll is None:
                # TODO: make an exception for threshold exceeded
                # log error
                raise Exception('Theshold for troll has exceeded')
            else:
                next_troll.send(submission)


    # gets the next troll to use if there is a threshold for submissions it
    # will skip over the trolls that have met the threshold, if there are no
    # trolls avialable it will yield none
    def _get_next_troll(self):
        # the troll we started the search on
        start_troll = None
        while True:
            for troll, thread in self.trolls.iteritems():
                # we have cycled through all of the trolls
                if troll == start_troll:
                    start_troll = None
                    yield None
                elif self.submission_threshhold == -1:
                    yield thread
                elif thread.get_submissions_left() < self.submission_threshhold:
                    yield thread
                # if we didn't find a troll to use we begin our search
                else:
                    start_troll = troll
