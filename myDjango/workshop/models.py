# encoding=utf-8

# -----------------------------------------------------------------
# File Name:        myDjango\models.py
# Description:      建立数据库表相关信息
# Function List:    创建数据库表
#
#
#
#
# -----------------------------------------------------------------


# Create your models here.
import datetime

from django.db import models
import json


class StaticInfo(models.Model):
    """
    机器静态信息表，存储一些机器出厂信息
    id:机器编号，no:机器型号，name:机器名称，date:生产时间
    """
    id = models.CharField(max_length=8, primary_key=True)
    no = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    date = models.DateField()  # 只存储日期
    objects = models.Manager()

    def save(self, *args, **kwargs):
        super(StaticInfo, self).save(*args, **kwargs)  # 调用父类save

    class Meta:
        db_table = 'StaticInfo'  # 表名
        verbose_name = "staticInfo"


class MachineInfo(models.Model):
    """
    工位具体信息表
    no:工位编号，id:判断是几号工位的什么状态, name:操作名, value:具体值和状态, time
    """
    # 如果没有models.AutoField，默认会创建一个id的自增列
    no = models.IntegerField()  # 工位编号
    update_time = models.DateTimeField(blank=True, primary_key=True)  # 操作时间，时间才是数据的唯一标识
    id = models.CharField(max_length=8)  # 操作唯一标识，但不是数据的唯一标识
    name = models.CharField(max_length=32)  # 操作分类名
    value = models.JSONField(default=dict)  # 具体的状态、数值等信息，采用json存储字典形式的数据
    objects = models.Manager()

    def save(self, *args, **kwargs):

        self.no = 1  # 固定为1
        # self.value = json.dumps(self.value)  # 将字典变为json格式，此操作会在双引号前增加转义反斜杠
        # self.time = (self.time.strftime('%Y-%m-%d %H:%M:%S'))  # 自定义日期格式
        super(MachineInfo, self).save(*args, **kwargs)  # 调用父类save

    class Meta:
        # ordering = ['time']
        db_table = 'MachineInfo'  # 表名
        verbose_name = "machineInfo"


class ImgInfo(models.Model):
    """
    照片信息表
    """
    tag = models.CharField(max_length=4)  # 照片类型，有'1':L1, '2':L2, '3':action, '4':reg, '5':result
    update_time = models.DateTimeField(blank=True, null=True)  # 创建时间
    id = models.CharField(max_length=8)
    data = models.ImageField()  # 图片内容数据
    name = models.CharField(max_length=16)
    value = models.CharField(max_length=64, primary_key=True)  # 文件名：path+日期+Tag+.jpg
    objects = models.Manager()

    class Meta:
        db_table = 'ImgInfo'  # 表名
        verbose_name = "imgInfo"

