#!/bin/sh

testg() {
    echo "$2"
    time sh -c "echo $2 | python3 game.py > res.txt"
    r=`tail -1 res.txt`
    test "X$r" = "X$1" || echo "$r" != "$1"
}

i=1
f=2

while true
do
    testg $i $f
    i=`expr $i + 1`
    f=`python3 -c "print($f * ($i + 1))"`
done

