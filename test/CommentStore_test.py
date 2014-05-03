import unittest
import csv

from CommentStore import comment_store

class TestCommentStore(unittest.TestCase):
    def setUp(self):
        self.comment_store = comment_store()
        self.troll = "Foo"
        self.chump = "bar"
        self.submissions_id = "baz"
        self.reponse_id = "qux"
        self.time = "some time"


    def test_store_comment(self):
        self.comment_store.store_comment(self.troll,
                                         self.chump,
                                         self.submissions_id,
                                         self.reponse_id,
                                         self.time)
        self.assertIn(self.chump, self.comment_store._comment_store_cache)
        self.assertTrue(self.comment_store._dirty)

    def test_writeback_one_comment_same_chump(self):
        '''
        the most trivial case. One chump to be trolled and one comment
        '''
        comment = {self.chump :
                   [self.troll, self.submissions_id, self.reponse_id, self.time]}
        self.comment_store._comment_store_cache = comment
        self.comment_store._write_to_file()
        with open('comment_store.csv', 'rb') as comment_file:
            commentread = csv.reader(comment_file, delimiter=',')
            try:
                line = next(commentread)
            except Exception:
                self.fail("comment store failed to create a file")
            self.assertEqual(self.chump,line[0])
            self.assertListEqual(comment[self.chump],line[1:])
        self.assertFalse(self.comment_store._dirty)

    def test_store_two_comments_one_chump(self):
        '''
        Adds two comments to the comment store for the same chump
        Only one comment should be written back to csv file

        '''
        self.comment_store.store_comment(self.troll,
                                         self.chump,
                                         self.submissions_id,
                                         self.reponse_id,
                                         self.time)
        self.comment_store.store_comment(self.troll,
                                         self.chump,
                                         self.submissions_id + "1",
                                         self.reponse_id,
                                         self.time)
        try:
            cs = self.comment_store._comment_store_cache[self.chump]
        except KeyError:
            self.fail("Comment Store insert failed")
        self.assertNotIn(self.submissions_id, cs)
        self.asertIn(self.submissions_id + "1", cs)
        self.asertTrue(self.comment_store._dirty)


    def test_comment_store_get_last_commment(self):
        comment = {self.chump :
                   [self.troll, self.submissions_id, self.reponse_id, self.time]}
        with open('comment_store.csv', 'wb+') as comment_file:
            commentwriter = csv.writer(comment_file, delimiter=',')
            commentwriter.writerow([self.chump] + comment[self.chump])

        last_comment = self.comment_store.get_last_trolled_comment(self.chump)
        self.assertEqual(self.submissions_id, last_comment)
        # clear the file after we use it, needs to be closed and re-opened so
        # the comment store can open the file to read to it
        with open('comment_store.csv', 'wb') as comment_file:
            comment_file.seek(0)
            comment_file.truncate()

    def test_writeback_does_not_overwrite_old_cache(self):
        '''
        Test to see if there is a writeback that the previously written data
        is still stored
        '''


