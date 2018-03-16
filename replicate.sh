#!/bin/sh

# a hundred thousand lines yields 40ms in urxvt, but 2.5 in xterm,
#
# a single line takes rxvt 9ms, which is small enough to be ignored in
# our tests, and is similar to xterm (10ms)
#
# ten times as much makes xterm take 30 seconds per test which meant
# 100 tests took 40 minutes, which was way too long
set -e
lines=100000
samples=100

echo "terminal,time,cpu,memory" >> times-${samples}x${lines}.csv

for terminal in uxterm xfce4-terminal konsole pterm ; do
    echo "priming $terminal"
    time $terminal -e "seq -f 'the quick brown fox jumps over the lazy dog %g' $lines"
    for i in $(seq $samples); do
        time $terminal -e "seq -f 'the quick brown fox jumps over the lazy dog %g' $lines" 2>> $terminal-time.txt
    done
    sed -n "/elapsed/{s/^.* 0:\([0-9]*.[0-9]*\)elapsed \([0-9?]*\)%CPU .*avgdata \([0-9]*\)maxresident.*\$/$terminal,\1,\2,\3/;p}" < $terminal-time.txt >> times-${samples}x${lines}.csv
done

# misquoted
for terminal in alacritty urxvt stterm mlterm; do
    echo "priming"
    time $terminal -e seq -f "the quick brown fox jumps over the lazy dog %g" $lines
    for i in $(seq $samples); do
        time $terminal -e seq -f "the quick brown fox jumps over the lazy dog %g" $lines 2>> $terminal-time.txt
    done
    sed -n "/elapsed/{s/^.* 0:\([0-9]*.[0-9]*\)elapsed \([0-9?]*\)%CPU .*avgdata \([0-9]*\)maxresident.*\$/$terminal,\1,\2,\3/;p}" < $terminal-time.txt >> times-${samples}x${lines}.csv
done
