#!/bin/sh

testg() {
    echo "$1"
    time sh -c "echo $1 | python3 game.py > res$PPID.txt"
    time sh -c "echo $1 | python3 game5.py > re5$PPID.txt"
    r=`tail -1 res$PPID.txt`
    r1=`tail -1 re5$PPID.txt`
    test "X$r" = "X$r1" || echo "$r" != "$r1"
}

i=1
f=2
m=3

while true
do
    testg $f
    i=`expr $i + 1`
    f=`python3 -c "print($f * $m)"`
    m=`python3 -c "print($m * 2)"`
    testg $f
    i=`expr $i + 1`
    f=`python3 -c "print($f * $m)"`
    m=`python3 -c "print($m * 3)"`
    testg $f
    i=`expr $i + 1`
    f=`python3 -c "print($f * $m)"`
    m=`python3 -c "print($m * 5)"`
done

