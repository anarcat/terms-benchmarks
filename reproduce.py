#!/usr/bin/python3

import argparse
from collections import defaultdict
import datetime
import logging
from multiprocessing import Process, Queue
import os
import subprocess
import time

import resource


def worker(terminal, cmd, queue):
    timer = Timer()
    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError as e:
            logging.warning('terminal %s failed with %s',
                            terminal, e)
            queue.put(False)
            return
    diff = timer.diff()
    res = resource.getrusage(resource.RUSAGE_CHILDREN)
    queue.put((res, diff))


def run_tests(terminal, cmd, samples):
    logging.info('priming terminal %s', terminal)
    logging.debug('running command %s', cmd)
    results = []
    try:
        subprocess.check_call(cmd)
    except FileNotFoundError:
        logging.warning('terminal %s not available, skipping', terminal)
        return results
    logging.info('running %d tests on %s', samples, terminal)
    for i in range(samples):
        queue = Queue()
        process = Process(target=worker, args=(terminal, cmd, queue))
        process.start()
        result = queue.get()
        process.join()
        logging.debug('result: %s', result)
        results.append(result)
    return results


class Timer(object):
    """this class is to track time

    golfed from ecdysis"""

    def __init__(self):
        """initialize the timstamp"""
        self.stamp = datetime.datetime.now()

    def diff(self):
        """a datediff between the creation of the object and now"""
        return datetime.datetime.now() - self.stamp

    def __str__(self):
        """return a string representing the time passed"""
        return 'elasped: %s' % str(self.diff())


def main():
    default_test_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'bw-test.sh'))
    parser = argparse.ArgumentParser()
    parser.add_argument('--lines', default=100000, type=int,
                        help='how many times to repeat the string')
    parser.add_argument('--samples', default=100, type=int,
                        help='how many tests to run')
    default_level = 'WARNING'
    parser.add_argument('-v', '--verbose',
                        dest='loglevel', action='store_const',
                        const='INFO', default=default_level,
                        help='enable verbose messages')
    parser.add_argument('-d', '--debug',
                        dest='loglevel', action='store_const',
                        const='DEBUG', default=default_level,
                        help='enable debugging messages')
    parser.add_argument('--loglevel',
                        default=default_level, type=str.upper,
                        help='expliticly set logging level')
    parser.add_argument('--wait', default=3, type=int,
                        help='time to wait before starting tests')
    parser.add_argument('--output', '-o',
                        help='output file for tests (default: times-SAMPLESxLINES.csv)')
    parser.add_argument('--terminal', nargs='*',
                        default=['konsole', 'pterm', 'terminator', 'uxterm', 'xfce4-terminal'],
                        help="terminals that need quoting %(default)s")
    parser.add_argument('--terminal-unquote', nargs='*',
                        default=['alacritty', 'mlterm', 'st', 'stterm', 'urxvt'],
                        help="terminals that do not need quoting %(default)s")
    parser.add_argument('--test', default=default_test_path,
                        help='test to run %(default)s')

    args = parser.parse_args()
    logging.basicConfig(format="%(levelname)s: %(message)s",
                        level=args.loglevel)

    if not args.output:
        args.output = 'times-%dx%d.csv' % (args.samples, args.lines)

    logging.info('disabling lock screen in all possible ways damnit')
    os.system('''gsettings set org.gnome.desktop.lockdown disable-lock-screen true
    gsettings set org.gnome.desktop.screensaver lock-enabled false
    gsettings set org.gnome.desktop.screensaver lock-delay 86400
    xset -dpms
    xset s off
    xset dpms 0 0 0 && xset s noblank && xset s off
    ''')

    logging.info('loading empty Xresources')
    os.system('xrdb -load /dev/null')

    logging.info('starting test in %d seconds, switch to a blank workspace',
                 args.wait)
    time.sleep(args.wait)

    logging.debug('writing to file %s', args.output)

    fields = ('ru_utime', 'ru_stime', 'ru_maxrss', 'ru_inblock', 'ru_oublock')
    i = 0

    with open(args.output, 'a') as csv:
        def write_result(terminal, result, diff):
            nonlocal i
            if not csv.tell():
                line = ['n', 'terminal', 'wtime']
                for field in fields:
                    line.append(field)
                csv.write(",".join(line) + "\n")

            line = [str(i), terminal, str(diff.total_seconds())]
            i += 1
            for field in fields:
                line.append(str(getattr(result, field)))
            csv.write(",".join(line) + "\n")

        for terminal in args.terminal:
            cmd = [terminal, '-e', "%s %d" % (args.test, args.lines)]
            for result, diff in run_tests(terminal, cmd, args.samples):
                write_result(terminal, result, diff)

        for terminal in args.terminal_unquote:
            cmd = [terminal, '-e', args.test, str(args.lines)]
            for result, diff in run_tests(terminal, cmd, args.samples):
                write_result(terminal, result, diff)

    logging.debug('resources: %s',
                  resource.getrusage(resource.RUSAGE_CHILDREN))


if __name__ == '__main__':
    main()
