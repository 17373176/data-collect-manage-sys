# encoding=utf-8

# -----------------------------------------------------------------
# File Name:        red.py
# Description:      相关操作
# Date:             2021/4/14
# License:          (C)Copyright 2021, Bob
# Function List:
#
#
# -----------------------------------------------------------------


import redis


if __name__ == "__main__":
    re = redis.Redis(host='127.0.0.1', password='123456', port='6379')
    re.set("key", "value")
    print(re.get('key'))

