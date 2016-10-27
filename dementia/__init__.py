'''
Dictionary with auto-expiring values for caching purposes.

Expiration happens on any access, object is locked during cleanup from expired
values. Can not store more than max_len elements - the oldest will be deleted.

>>> Dementia(max_len=100, max_age=10)

The values stored in the following way:
{
    key1: (value1, created_time1),
    key2: (value2, created_time2)
}

The pool_time parameter (default 5 minutes or 60*5 seconds) controls how often
the cache is cleared of old values.
'''
import sys
import datetime
from threading import RLock
from collections import defaultdict


class Dementia(dict):
    def __init__(self, *args, **kwargs):
        if 'max_len' in kwargs:
            self.max_len = kwargs['max_len']
            del kwargs['max_len']
        else:
            self.max_len = -1

        if 'max_age' in kwargs:
            self.max_age = kwargs['max_age']
            del kwargs['max_age']
        else:
            self.max_age = -1

        if 'pool_time' in kwargs:
            self.pool_time = kwargs['pool_time']
            del kwargs['pool_time']
        else:
            self.pool_time = self.max_age

        self.lock = RLock()
        self.__set_check_time()
        self.update(*args, **kwargs)

    def __getitem__(self, key):
        with self.lock:
            val = dict.__getitem__(self, key)
            self.Usage[key] += 1
            self.__purge()
        return val

    def __setitem__(self, key, val):
        with self.lock:
            if self.max_len > 0:
                if len(self) == self.max_len:
                    self.__remove_least_used()
            self.__purge()
            dict.__setitem__(self, key, val)
            self.Usage[key] = 1

    def update(self, *args, **kwargs):
        with self.lock:
            for k, v in dict(*args, **kwargs).items():
                self[k] = v

    def __set_check_time(self):
        with self.lock:
            self.check_time = datetime.datetime.now() + \
                datetime.timedelta(seconds = self.pool_time)
            self.Usage = defaultdict(int)

    def __remove_least_used(self, thresh=None):
        '''Checks the number of elements. If too many, remove least used.
        '''
        def argmin(z, thresh=None):
            if not z: return None
            min_val = min(z.values())
            if thresh:
                if min_val <= thresh:
                    return None
            else:
                return [k for k in z if z[k] == min_val][0]

        with self.lock:
            purge = argmin(self.Usage, thresh)
            if purge:
                print('removing {} because of usage: {}'.format(purge, self.Usage[purge]))
                del self[purge]
                del self.Usage[purge]

    def __purge(self):
        if self.max_age > 0:
            if datetime.datetime.now() >= self.check_time:
                self.__remove_least_used(thresh=0)
                self.__set_check_time()

