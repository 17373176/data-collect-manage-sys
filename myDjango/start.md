% start.md
## 运行环境部署
### Python-3.7、PyCharm Community-2018安装(也可使用专业版)
•使用pip 安装django：pip install django；
•创建Django project：django-admin startproject myDjango；
•使用PyCharm打开myDjango，在project中设置解释器，安装Django。
•创建APP：python manage.py startapp workshop，把该文件目录加入到settings文件中的installed_apps列表里
•admin后台帐号密码：python manage.py createsuperuser； root/123456邮箱：1@qq.com

### OPC UA客户端及OpenSSL部署
•安装opcua包，安装OpenSSL
•生成CA密钥：openssl genrsa -out ca_key.pem 1024
•创建CA证书：openssl req -new -out ca_req.csr -key ca_key.pem
•生成自签名：openssl x509 -req -in ca_req.csr -out ca_cert.pem -signkey ca_key.pem -days 365
•再根据CA分别生成服务器和客户端证书、私钥openssl x509 -req -in server_req.csr -out server_cert.pem -signkey server_key.pem -CA ca_cert.pem -CAkey ca_key.pem -CAcreateserial -days 365

### MySQL-8.0.23-winx64部署
•解压缩包
•配置环境变量，变量名：MYSQL_HOME；变量值：D:\mysql-x64；
•cd到目录D:\mysql-x64\bin下，执行mysqld --initialize-insecure --user=mysql在上一目录下生成data目录，如果是在PowerShell需要在命令前加“.\”；
•安装：mysqld -install；（如果denied，则启动管理员运行）
•启动服务：net start mysql
•登录MySQL：mysql -u root -p （默认没设置密码，直接回车）
用户名/密码：root/123456
默认端口：127.0.0.1:3306
数据库名称：local_db

### Redis-5.0部署
•解压，在目录下执行启动服务：redis-server.exe redis.windows.conf  启动后不要关闭cmd，保持启动状态

•新打开cmd窗口，执行：redis-cli 连接默认本机端口号127.0.0.1:6379

•将Redis 加入 Windows 服务，执行：redis-server --service-install redis.windows.conf

•密码：123456取消了密码
•默认端口：127.0.0.1:6379 

### Kafka部署
•pip安装即可
•启动kafka内置的zookeeper: zookeeper-server-start.bat  ..\..\config\zookeeper.properties，不要关闭窗口，再打开一个
•在安装目录bin\windows目录下启动kafka服务：kafka-server-start.bat ..\..\config\server.properties
•端口号zookeeper：2181；kafka：9092
如果出现ERROR Shutdown broker错误则删除log文件，重新启动



## 启动后端项目
启动服务：在cmd命令行下输入：python manage.py runserver 0.0.0.0:8000