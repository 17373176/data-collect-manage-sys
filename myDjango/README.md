% README.md
# Django框架开发

## dir-cert
OPC UA协议服务端和客户端相关证书、私钥

## db.aqlite3
Django默认生成的数据库文件

## manage.py 
可以理解为他是django应用的控制中心，许多命令的实现，都需要他来调动。

## dir-myDjango
 
init.py:这是一个初始化的空文件，一般我们不需要动它

settings.py:这是一个配置文件，里面有关于语言、时区、安装的app声明等等信息；
修改默认数据库为MySQL


urls.py:这个文件里指明了在访问一个页面时要调用的视图函数的路径映射，确保在访问时可以正确定位到你要实现的功能；URL的加载是从配置文件中开始

wsgi.py:这是一个关于web程序的wsgi的相关配置，我们暂时不需要修改它。


## dir-dataAcquisition
数据采集、协议传输部分，接收数据后放入消息队列(本地单机)中，以便于持久化操作

## dir-workshop
### dir-migrations
存放数据库操作日志文件的目录

### MVC-model(模型),view(视图),controller(控制器)
model: 管理应用程序的状态（通常存储到数据库中），约束改变状态的行为

view:负责把数据格式化后呈现给用户，或者收到用户请求

controller:接受外部用户的操作，根据操作访问模型获取数据，并调用“视图”显示这些数据。控制器是将“模型”和“视图”隔离，并成为二者之间的联系纽带

Django也是一个MVC框架，但是在Django中，控制器接受用户输入的部分由框架自行处理，所以 Django 里更关注的是模型（Model）、模板(Template)和视图（Views），称为 MTV

Model：即数据存取层。该层处理与数据相关的所有事务：如何存取、如何验证有效性、包含哪些行为以及数据之间的关系等。

Template：即表现层。该层处理与表现相关的决定：如何在页面或其他类型文档中进行显示。例如html文件

View：即业务逻辑层。该层包含存取模型及调取恰当模板的相关逻辑。可以把它看作模型与模板之间的桥梁。


models.py：模型文件，建表，编写数据库相关操作函数（类似于Dao文件）。

forms.py：文件上穿下载相关操作

views.py：主要把数据推给前端，或者编写接口给对方调用。Django是在views.py文件中，通过导入models.py文件来创建数据的：


## dir-static
相关图片的保存，文件夹名称对应：loading-托盘照片、reg-良品/不良品、action-装配动作、result-装配结果




