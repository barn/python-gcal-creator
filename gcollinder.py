#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# -----------------------------------------------------------
# Filename      : gcollinder.py
# Description   : Converting a human ish string, in to a google calendar URL.
#                 Poorly recreating the "Create Event" that no longer exists ):
# Created By    : Bea Hughes
# Date Created  : 2020-02-24 22:02
#
# License       : MIT
# -----------------------------------------------------------
#
# have a python 3 like print() for stderr writing as a little treat
from __future__ import print_function
from future import standard_library

from builtins import str
from builtins import object
import re
import sys
import urllib
import webbrowser
from dateparser.search import search_dates
from datetime import datetime as dt
from datetime import timedelta

__author__ = "Bea Hughes"
__version__ = "0.2"

standard_library.install_aliases()


class Entry(object):

    DEFAULT_EVENT_DUR = timedelta(minutes=30)

    MIDNIGHT = dt.time(dt(1979, 1, 1, 0, 0))

    RE = re.compile(r"""
                    \b (?P<location>in \s+ .+) ($|\bat\b)
                    """, re.X)

    def __init__(self, raw):
        self.raw = str(raw)
        self.__parse__()

    def __parse__(self):

        event = self.raw

        self.dates = search_dates(event,
                                  languages=['en'],
                                  settings={'DATE_ORDER': 'DMY'})
        if self.dates is None:
            print("No dates found, boo", file=sys.stderr)
            sys.exit(10)

        event = ''.join({event.replace(str(atuple[0]), '')
                        for atuple in self.dates})
        event = re.sub(r"\s\s", " ", event)
        self.text = event

        # If we can grab a location (has 'in <location>' in it), then set the
        # location and remove that from the event text/title.
        self.location = ''
        r = self.RE.search(self.raw)
        if r:
            self.location = r.group('location')

    def url(self):
        # URL format something like
        # http://www.google.com/calendar/event?ctext=+{query}+&action=TEMPLATE&pprop=HowCreated%3AQUICKA
        # Format is [event] at [time] on [date] in [location]

        # https://calendar.google.com/calendar/render?action=TEMPLATE&
        #  text=foo&
        #  dates=20170101T270000Z/20170101T280000Z&
        #  details=Describe your event.&
        #  location=Event Location&
        #  trp=true
        base = 'https://calendar.google.com/calendar/render'
        quer = {'action': 'TEMPLATE',
                'text': self.text,
                # 'dates': self.dates,  # this now comes from a function()
                'location': self.location,
                'trp': True}

        # go off and beat the date guessed in to the format we want.
        # returns a Dict of date/dates: <format o dates>
        x = self.fixate_dates()
        quer.update(x)

        # Python 2:
        self.uri = base + '?' + urllib.parse.urlencode(quer)
        return self.uri

    # Actually open it in a web browser
    def open_url(self):
        print("opening " + str(self.uri))
        webbrowser.open(self.uri)

    # dateparser will return some date/times grabbed from the input. It will do
    # it's best to make sense. This is the function that does that. A lot of
    # gross magic happens here.
    # returns a Dict of date/dates: <format o dates>
    def fixate_dates(self):

        if len(self.dates) == 1:

            lone_date = self.dates[0][1]
            if dt.time(lone_date) == self.MIDNIGHT:
                # this blindly assumes I do nothing at midnight. I know.
                # all day event, just has the day.
                x = {'date': d(lone_date)}
            else:
                # regular event, put a finish time of whatever duration we set,
                # so it knows how long to make the event.
                d2 = lone_date + self.DEFAULT_EVENT_DUR
                x = {'dates': d(lone_date) + '/' + d(d2)}
        elif len(self.dates) == 2:
            # having two dates could mean it guessed at two, or there is a
            # start and a finish. Bleh.
            d1 = self.dates[0][1]
            d2 = self.dates[1][1]

            f = self.__fucky__(d1, d2)
            if f is not False:
                print('fudging dates a bunch.')
                fudge = f + self.DEFAULT_EVENT_DUR
                x = {'dates': d(f) + '/' + d(fudge)}

        return x

    # we don't necessarily know the order here, as it depends how dateparser
    # does, so it could be one way, it could be the other, hence this
    # abomination.
    def __fucky__(self, d1, d2):
        for x, y in list({d1: d2, d2: d1}.items()):
            if dt.time(x) == self.MIDNIGHT \
               and dt.date(y) == dt.date(dt.today()):
                # actually return a dt object with the date from x and the time
                # from y (the inverse of what we check for)
                return dt.combine(dt.date(x), dt.time(y))
        return False


# gross helper to return the time in the format gcal wants.
# make it 20170101T270000Z format. Kinda here so it can have a shorter name.
def d(a_date):
    return(a_date.strftime('%Y%m%dT%H%M%S%Z'))


def something():

    if len(sys.argv) < 2:
        line = sys.stdin.readline()
    else:
        line = ' '.join(sys.argv[1:])

    if not line:
        return

    e = Entry(line)

    print(e.url())


if __name__ == "__main__":
    something()
