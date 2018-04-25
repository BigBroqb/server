from datetime import datetime
from threading import Timer

import subprocess
import pytz


def is_equal(mo1, mo2):
    if (mo1.comm == mo2.comm) and (mo1.dt == mo2.dt):
        return True
    return False


class Monitor:
    '''Class to manage scheduled events'''
    def __init__(self, s, user, func, dt):
        self.schedule = s
        self._running = False
        self.func = func
        self.user = user
        self.dt = dt

    def __str__(self):
        return str(self.dt)

    def get_info(self):
        return self.user

    def send(self, user, func, _):
        func(user)
        return

    def scheduleJob(self):
        user = self.user
        func = self.func
        dt = self.dt
        timezone = pytz.timezone("US/Eastern")
        # time_start = (dt-datetime(1970, 1, 1)).total_seconds()
        self.t = Timer((dt-timezone.localize(datetime.now())).total_seconds(),
                       self.send, args=(user, func, 0))
        self.t.start()
        # print(comm+" Job scheduled at " + datetime.strftime(dt, '%c'))

    def start(self):
        self._running = True
        self.scheduleJob()

    def stop(self):
        self._running = False
        if self.t:
            self.t.cancel()
