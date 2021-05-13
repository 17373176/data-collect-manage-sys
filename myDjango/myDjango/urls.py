"""myDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# -----------------------------------------------------------------
# File Name:        myDjango\urls.py
# Description:      配置相应函数路径映射
# Function List:
# -----------------------------------------------------------------

from django.contrib import admin
from django.urls import path, include

# 可以利用正则表达式匹配url,也可以使用二级路由
urlpatterns = [
    path('admin/', admin.site.urls),  # 采用单正斜杠作目录，则不需要加r，如果是单反斜杠则需要加r，否则得用双反斜杠
    path('workshop/', include('workshop.urls')),  # 包含workshop里面的urls，才能执行workshop/urls.py里的路径
    path('dataAcquisition/', include('dataAcquisition.urls')),


]
