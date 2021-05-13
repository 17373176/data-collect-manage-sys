# !/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

# encoding=utf-8

# -----------------------------------------------------------------
# File Name:        manage.py
# Description:      启动服务
# Function List:
#                   建空间 -- idx
#                   获取点 -- objects
#                   完成间的映射
#                   开器 -- start()
#                   为前端提供API接口，对方能够从数据库和云获取数据
#
# 在该目录终端执行:  python manage.py runserver 0.0.0.0:8000
# 在浏览器输入:      localhost:8000访问
# -----------------------------------------------------------------

import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myDjango.settings')
    try:
        from django.core.management import execute_from_command_line

        """import channels.layers
        channel_layer = channels.layers.get_channel_layer()
        from asgiref.sync import async_to_sync
        async_to_sync(channel_layer.send)('test_channel', {'type': 'hello'})
        async_to_sync(channel_layer.receive)('test_channel')
        """

    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
