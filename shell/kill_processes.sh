#!/bin/bash
currentPid=$$
ps -aux | grep "/usr/sbin/httpd" | grep -v "grep" | awk '{print $2}' > /tmp/${currentPid}.txt
for pid in `cat /tmp/${currentPid}.txt`
do
{
    echo "kill -9 $pid"
    kill -9 $pid
}
done
rm -f /tmp/${currentPid}.txt
