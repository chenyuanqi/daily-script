#!/bin/bash
# 获取随机字符串和数字
echo "8 位随机字符串："
echo $RANDOM | md5sum | cut -c 1-8
echo "8 位随机数字："
echo $RANDOM |cksum |cut -c 1-8
