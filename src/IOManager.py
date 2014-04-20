import threading
from Queue import Queue
class IOManager():
    def __init__(self, passwords_file_path, data_file_path):
        #OPEN FILEs and stuff 
        self.writer = WriterThread(data_file=self.data_file)

    def write(write_object):
        '''
        writes 
        '''
        pass
    
    def get_logins(number_logins):
        pass

    def get_most_recent_comment(chump):
        pass

class WriterThread(threading.Thread):
    '''
Wrapper for IO bound operations 
Read/Writes to two files, one for passwords and usernames for Autotrolls  (txt)
One that contains data about previously trolled comments (xml)
Wrapper only 
   
   usage : 
    iothread = IOThread(passwords_file='passwords.txt', storage_file='storage_file.xml')
    iothread.send(thing)
    iothread.close()
    '''
    def __init__(self, *args, **kwargs):
        self.input_queue = Queue()
    def write(self, item):
        self.input_queue.put(item)
    def close(self):
        self.data_file.close()
        self.input_queue.put(None)
        self.input_queue.join()
    def run(self):
        while True:
            item  = self.input_queue.get()
            if item is None:
                break
            #process item
            self.input_queue.task_done()
        self.input_queue.task_done()
        return
