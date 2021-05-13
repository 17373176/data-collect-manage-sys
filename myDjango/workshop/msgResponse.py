# encoding=utf-8

# -----------------------------------------------------------------
# File Name:        msgResponse.py
# Description:      提示相关信息
# Function List:    成功信息
#                   错误信息
#                   Json信息
#                   数据库连接失败
#                   数据库操作异常异常
#                   云服务器连接失败
#
#
#
# -----------------------------------------------------------------


class ExceptionHandle(Exception):  # 继承父类Exception
    def __init__(self, msg, op):
        """
        异常处理
        @param msg: 异常信息
        @param op: 异常类型
        """
        if op == 'db_conn_failed':  # is是用来判断是否引用同一个对象，和equal相似
            Exception.__init__(self, '数据库连接失败：' + msg)
        elif op == 'db_op_error':
            Exception.__init__(self, '数据库操作异常：' + msg)
        elif op == 'data_server_con_failed':
            Exception.__init__(self, '数据采集服务器连接失败：' + msg)
        else:
            Exception.__init__(self, '其他异常：' + msg)


def exception_msg(e, msg):
    print(msg)
    return e


def success_msg(msg_detail=None):
    """
    成功信息
    @param msg_detail:
    @return: dict
    """
    r = {'result': 'success'}
    if msg_detail:
        r['detail'] = msg_detail
    else:
        r['detail'] = {}
    return r


def error_msg(err_msg=None):
    """
    错误信息
    @param err_msg:
    @return: dict
    """
    r = {'result': 'error',
         'detail': {
             'error_msg': err_msg
         }}
    return r
