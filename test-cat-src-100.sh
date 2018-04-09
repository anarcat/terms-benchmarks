#!/bin/sh

# this is another test to replicate the results from the xterm
# benchmark
for i in $(seq 100); do cat /home/anarcat/dist/ncurses-6.1+20180210/misc/terminfo.src; done
