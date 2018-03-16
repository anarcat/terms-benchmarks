#!/usr/bin/python3

# apt install python3-seaborn

import argparse
import datetime
import logging
import os
import sys

import seaborn as sns
import matplotlib.pyplot as plt
import pandas
# import numpy as np


class Timer(object):
    """this class is to track time and resources passed"""

    def __init__(self):
        """initialize the timstamp"""
        self.stamp = datetime.datetime.now()

    def times(self):
        """return a string designing resource usage"""
        return 'user %s system %s chlduser %s chldsystem %s' % os.times()[:4]

    def diff(self):
        """a datediff between the creation of the object and now"""
        return datetime.datetime.now() - self.stamp

    def __str__(self):
        """return a string representing the time passed and resources used"""
        return 'elasped: %s (%s)' % (str(self.diff()), self.times())


logging.basicConfig(format='%(message)s', level=logging.DEBUG)
parser = argparse.ArgumentParser()
parser.add_argument('--output', type=argparse.FileType('wb'),
                    default=sys.stdout,
                    help='image to write (default to terminal if available, otherwise stdout)')
args = parser.parse_args()
timer = Timer()

logging.debug('starting, %s', timer)
sns.set_style("whitegrid")

ignored_terms = ['xvt',  # rare
                 'eterm',  # too old
                 'kterm',  # too old
                 'mrxvt',  # mostly like rxvt
                 'xfce4-terminal',  # like gnome-terminal
                 'xfce4',  # synonym
                 'terminator',  # synonym
                 'Terminator']  # like gnome-terminal


resources = pandas.read_csv('performance.csv')
logging.debug('loaded performance.csv, elasped: %s', timer)

for terminal in ignored_terms:
    resources = resources[resources.terminal != terminal]  # rare
resources = resources.sort_values(by='time (s)')
print(resources)

g = sns.PairGrid(resources,
                 x_vars='terminal',
                 y_vars=['time (s)', 'cpu (%)', 'memory (k)'])
g.map(sns.barplot, palette="colorblind")

#i = 0
#for param, title in [('time (s)', 'wall clock run time'),
#                     ('cpu (%)', 'CPU usage'),
#                     ('memory (k)', 'memory usage')]:
#    ax = sns.barplot(data=resources.sort_values(by=param),
#                     y=param, x='terminal',
#                     ax=plt.subplot(grid[1, i]))
#    i += 1
#    ax.set_title(title)

if args.output == sys.stdout and \
        ('DISPLAY' in os.environ or sys.stdout.isatty()):
    logging.info("drawing on tty, %s", timer)
    plt.show()
else:
    logging.info('drawing to file %s, %s', args.output, timer)
    _, ext = os.path.splitext(args.output.name)
    plt.savefig(args.output, format=ext[1:])
logging.debug('completed %s', timer)
