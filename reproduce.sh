#!/bin/sh

set -e

# how many times to repeat the string
lines=100000

# how many tests to run
samples=100

test="$PWD/bw-test.sh $lines"

echo "setting Xresources to defaults"
xrdb -load /dev/null

echo "terminal,time,cpu,memory" >> times-${samples}x${lines}.csv

for terminal in konsole pterm terminator uxterm xfce4-terminal  ; do
    echo "priming $terminal"
    time $terminal -e "$test"
    for i in $(seq $samples); do
        time $terminal -e "$test" 2>> $terminal-time.txt
    done
    sed -n "/elapsed/{s/^.* 0:\([0-9]*.[0-9]*\)elapsed \([0-9?]*\)%CPU .*avgdata \([0-9]*\)maxresident.*\$/$terminal,\1,\2,\3/;p}" < $terminal-time.txt >> times-${samples}x${lines}.csv
done

# misquoted
for terminal in alacritty mlterm stterm urxvt; do
    echo "priming"
    time $terminal -e $test $lines
    for i in $(seq $samples); do
        time $terminal -e $test $lines 2>> $terminal-time.txt
    done
    sed -n "/elapsed/{s/^.* 0:\([0-9]*.[0-9]*\)elapsed \([0-9?]*\)%CPU .*avgdata \([0-9]*\)maxresident.*\$/$terminal,\1,\2,\3/;p}" < $terminal-time.txt >> times-${samples}x${lines}.csv
done

echo "resetting Xresources"
xrdb -load ~/.Xresources
