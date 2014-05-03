#Auto Troll
#Author: Ace Levenberg (acelevenberg@gmail.com)
#----------------------------------------------------------------------------
#"THE BEER-WARE LICENSE" (Revision 42):
#<acelevenberg@gmail.com> wrote this file. As long as you retain this notice you
#can do whatever you want with this stuff. If we meet some day, and you think
#this stuff is worth it, you an buy me a beer in return Ace Levenberg
#----------------------------------------------------------------------------

import csv

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
    '''
    def __init__(self, data_file_path='comment_store.csv'):
        #OPEN FILEs and stuff
        self._dirty = True
        self._comment_store_cache = dict()

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
        pass

    def get_last_trolled_comment(self,chump):
        '''
        Gets the last comment that  has been trolled in the data_file for the given chump
        params:
            the chump to get the most recent comment
        returns:
           the last comment to be trolled
        '''
        pass

    def _write_to_file(self):
        """
        writes the cache back to file
        """
        pass
