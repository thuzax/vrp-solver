import sys
import time
import multiprocessing
import threading

from src import exceptions
from src import execution_log

class TimelimitedThread(threading.Thread):
    def __init__(self, *args, time_limit, **kwargs):
        self.time_limit = time_limit
        self._run_backup = self.run  # Save superclass run() method.
        self.run = self._run  # Change it to custom version.
        self.time_limit_exceeded = False
        super().__init__(*args, **kwargs)

    def _run(self):
        self.start_time = time.time()
        sys.settrace(self.globaltrace)
        self._run_backup()  # Call superclass run().
        self.run = self._run_backup  # Restore original.

    def globaltrace(self, frame, event, arg):
        return self.localtrace if event == 'call' else None

    def localtrace(self, frame, event, arg):
        if(event == 'line' and
           time.time()-self.start_time > self.time_limit):  # Over time?
            self.time_limit_exceeded = True
            raise SystemExit()  # Terminate thread.
        return self.localtrace


class TimeOut(object):
    instance = None
    created = False
    
    def __new__(cls, *args, **kwargs):
        if (cls.instance is None):
            cls.instance = super(TimeOut, cls).__new__(cls)
            cls.time_limit = None
        
        return cls.instance

    def __init__(self, time_limit=None):
        if (self.time_limit is None):
            self.time_limit = time_limit

        super().__init__()


    def run(self, function):
        self.exec = TimelimitedThread(
            target=function, 
            time_limit=self.time_limit
        )

        self.exec.start()
        self.exec.join()
        if (self.exec.time_limit_exceeded):
            raise exceptions.TimeLimitExceeded