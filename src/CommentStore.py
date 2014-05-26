#Auto Troll
#Author: Ace Levenberg (acelevenberg@gmail.com)
#----------------------------------------------------------------------------
#"THE BEER-WARE LICENSE" (Revision 42):
#<acelevenberg@gmail.com> wrote this file. As long as you retain this notice you
#can do whatever you want with this stuff. If we meet some day, and you think
#this stuff is worth it, you an buy me a beer in return Ace Levenberg
#----------------------------------------------------------------------------

import csv
import os
import shutil

from threading import Lock
from tempfile import mkstemp

__comment_sotre = None
def comment_store():

   """
    comment store singleton
    default comment_store.csv
   """
   if __comment_sotre is None:
        __comment_store = CommentStore()
   return __comment_store

class CommentStore():

    '''
    Stores comments that have been made
    the constructor for this object should never be called.
    instead the  singleton should be used because of the lock object
    '''
    def set_data_path(self, data_path):
        self.data_file_path = data_path

    def __init__(self, data_file_path='comment_store.csv'):
        self._dirty = False
        self._comment_store_cache = dict()
        self.lock = Lock()
        self.data_file_path = data_file_path

    def store_comment(self,troll, chump, submissions_id, reponse_id, time):
        '''
        stores the trolled comment into the data file
        params:
                troll(string) the troll that made the comment
                chump(string) the chump that got trolled
                submissions_id(string) the actual comment that was trolled
                reponse_id(string) the id of the response
                time the time the resposne was made
        '''
        comment = [troll,submissions_id, reponse_id, time]
        self._add_coment(chump, comment)
        self._dirty = True

    # unlocks the lock object inserts the comment in the cache
    def _add_coment(self,chump,comment):
        with self.lock:
            self._comment_store_cache[chump] = comment

    def get_last_trolled_comment(self,chump):
        '''
        Gets the last comment that  has been trolled in the data_file for the given chump
        params:
            the chump to get the most recent comment
        returns:
           the last comment/submission id to be trolled
        '''
        with self.lock:
            if chump in self._comment_store_cache:
                return self._comment_store_cache[chump][1]
        for line in self._read_from_file(self.data_file_path):
            # add all of the chumnps we see to the cache
            with self.lock:
                self._comment_store_cache[line[0]] = line[1:]
            if line[0] == chump:
                return self._comment_store_cache[line[0]][1]


    def get_stored_chumps(self):
        """
        Gets the next chump in line
        params:
            None
        returns:
            a generator object of chumps all read from the csv file
        """
        for line in self._read_from_file(self.data_file_path):
            chump = line[0]
            with self.lock:
                if chump not in self._comment_store_cache:
                    self._comment_store_cache[chump] = line[1:]
            yield chump



    def _write_to_file(self):
        """
        writes the cache back to file
        """
        # No neec to write if nothing has changed from the file
        if not self._dirty:
            return
        _ , path = mkstemp()
        tempfile = open(path, 'wb+')
        commentwriter = csv.writer(tempfile, delimiter=',')
        with self.lock:
            for line in self._read_from_file(self.data_file_path):
                if line[0] in self._comment_store_cache:
                    commentwriter.writerow([line[0]] + \
                                            self._comment_store_cache[line[0]])
                    del self._comment_store_cache[line[0]]
                else:
                    commentwriter.writerow(line)
            for chump, comment in self._comment_store_cache.iteritems():
                        commentwriter.writerow([chump] + comment )
        #os.remove(self.data_file_path)
        shutil.move(path, self.data_file_path)
        tempfile.close()
        self._dirty = False

    def _read_from_file(self, file_to_read):
        '''
        returns a generator object that generates the
        lists in the given file
        '''
        if not os.path.exists(file_to_read):
            return
        with open(file_to_read, 'rb') as comment_file:
            commentreader = csv.reader(comment_file, delimiter=',')
            # maybe the comment reader should just be returned...
            # as it is a generator (i think)
            # this isn't really that helpful
            for row in commentreader:
                yield row

