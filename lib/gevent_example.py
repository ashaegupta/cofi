#!/usr/bin/env python

from gevent import monkey; monkey.patch_all()
import gevent
import json
import time

yelp_url = ""
fs_url = ""


def timed(f):
    def wrapped(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        print 'Took', end - start, 'seconds...'
        return result
    return wrapped

def fetch(pid):
    print "Starting to fetch", pid
    start = time.time()
    response = requests.get('https://www.google.com/images/srpr/logo3w.png')
    end = time.time()
    print "Got result", pid, "in", end - start, "seconds."
    return response

@timed
def synchronous():
    for i in range(10):
        fetch(i)

@timed
def asynchronous():
    jobs = []
    for i in range(2):
        jobs.append(gevent.spawn(fetch, i))
    gevent.joinall(jobs)
    return jobs

@timed
def async_2():
    pile = gevent.GreenPile(pool)
    for h in hostnames:
        pile.spawn(_setup_a_cannon, h)
    responses = list(pile)
    print 'Done!'
    

#print "Synchronous:"
#synchronous()

print "Asynchronous:"
asynchronous()
