import unittest
import csv
import os

from CommentStore import comment_store

class TestCommentStore(unittest.TestCase):
    def setUp(self):
        self.comment_store = comment_store()
        self.data_store_file = os.path.abspath("comment_store_test.csv")
        self.comment_store.set_data_path(self.data_store_file)
        self.troll = "Foo"
        self.chump = "bar"
        self.submissions_id = "baz"
        self.reponse_id = "qux"
        self.time = "some time"

    def tearDown(self):
        if os.path.exists(self.data_store_file):
            os.remove(self.data_store_file)
        self.comment_store._comment_store_cache = None
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
        comment = [self.troll, self.submissions_id, self.reponse_id, self.time]
        self.comment_store._comment_store_cache[self.chump] = comment
        self.comment_store._dirty = True
        self.comment_store._write_to_file()
        with open(self.data_store_file, 'rb') as comment_file:
            commentread = csv.reader(comment_file, delimiter=',')
            try:
                line = next(commentread)
            except Exception:
                self.fail("comment store failed to write to file")
            self.assertEqual(self.chump,line[0])
            self.assertListEqual(comment,line[1:])
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
        self.assertIn(self.submissions_id + "1", cs)
        self.assertTrue(self.comment_store._dirty)

    def test_read_from_file(self):
        comment = {self.chump :
                   [self.troll, self.submissions_id, self.reponse_id, self.time]}
        with open(self.data_store_file, 'wb+') as comment_file:
            commentwriter = csv.writer(comment_file, delimiter=',')
            commentwriter.writerow([self.chump] + comment[self.chump])
            commentwriter.writerow([self.chump + "eggs"] + comment[self.chump])
        try :
            csvfile = self.comment_store._read_from_file(self.data_store_file)
            line_one = csvfile.next()
            self.assertIn(self.chump, line_one)
            line_two = csvfile.next()
            self.assertIn(self.chump + "eggs", line_two)
        except Exception:
            self.fail("Data was not read properly from file")

    def test_comment_store_get_last_commment(self):
        comment = {self.chump :
                   [self.troll, self.submissions_id, self.reponse_id, self.time]}
        with open(self.data_store_file, 'wb+') as comment_file:
            commentwriter = csv.writer(comment_file, delimiter=',')
            commentwriter.writerow([self.chump] + comment[self.chump])

        last_comment = self.comment_store.get_last_trolled_comment(self.chump)
        self.assertEqual(self.submissions_id, last_comment)

    def test_comment_store_get_next_chump(self):
        comment = {self.chump :
                   [self.troll, self.submissions_id, self.reponse_id, self.time]}
        with open(self.data_store_file, 'wb+') as comment_file:
            commentwriter = csv.writer(comment_file, delimiter=',')
            commentwriter.writerow([self.chump] + comment[self.chump])
            commentwriter.writerow([self.chump + "eggs"] + comment[self.chump])
        chump_names = [self.chump, self.chump + "eggs"]
        for chump in self.comment_store.get_stored_chumps():
            self.assertIn(chump, chump_names)

    def test_writeback_does_not_overwrite_old_cache(self):
        '''
        Test to see if there is a writeback that the previously written data
        is still stored
        '''
        comment = [self.troll, self.submissions_id, self.reponse_id, self.time]
        with open(self.data_store_file, 'wb+') as comment_file:
            commentwriter = csv.writer(comment_file, delimiter=',')
            commentwriter.writerow([self.chump] + comment)
        self.comment_store._comment_store_cache[self.chump+"eggs"] = [self.troll,
                                                                    self.submissions_id + "spam",
                                                                    self.reponse_id,
                                                                    self.time]
        self.comment_store._dirty = True
        self.comment_store._write_to_file()
        with open(self.data_store_file, 'rb') as comment_file:
            try:
                commentreader = csv.reader(comment_file, delimiter=',')
                line_one = commentreader.next()
                self.assertIn(self.chump, line_one)
                self.assertIn(self.submissions_id, line_one)
                line_two = commentreader.next()
                self.assertIn(self.chump + "eggs", line_two)
                self.assertIn(self.submissions_id + "spam", line_two)
            except Exception as e:
                self.fail(str(e))

    def test_writeback_does_not_write_removed_chump(self):
        comment = [self.troll, self.submissions_id, self.reponse_id, self.time]
        with open(self.data_store_file, 'wb+') as comment_file:
            commentwriter = csv.writer(comment_file, delimiter=',')
            commentwriter.writerow([self.chump] + comment)
        self.comment_store._comment_store_cache[self.chump+"eggs"] = [self.troll,
                                                                    self.submissions_id + "spam",
                                                                    self.reponse_id,
                                                                    self.time]
        self.comment_store._dirty = True
        self.comment_store._write_to_file()
        self.comment_store.remove_chump(self.chump + "eggs")
        self.comment_store._write_to_file()
        with open(self.data_store_file, 'rb') as comment_file:
            commentreader = csv.reader(comment_file, delimiter=',')
            line_one = commentreader.next()
            self.assertIn(self.chump, line_one)
            self.assertIn(self.submissions_id, line_one)
            with self.assertRaises(Exception):
                next(commentreader)








