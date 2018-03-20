#!/bin/sh

set -e

# how many times to repeat the string
lines=100000

# how many tests to run
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
