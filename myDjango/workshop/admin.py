from django.contrib import admin

# Register your models here.
from workshop import models

# 将models.py里创建的表加入后台管理中
admin.site.register(models.MachineInfo)
admin.site.register(models.StaticInfo)
admin.site.register(models.ImgInfo)

