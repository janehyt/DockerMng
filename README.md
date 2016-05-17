MyWeb
=====
#首先构建前端页面
1. 首先安装node（>4.2）
2. 再全局安装gulp npm install --global gulp
3. 在webapp目录下执行gulp

#再启动django服务
##不通过Docker
1. 建立virtualenv环境
2. 进入独立python环境后执行pip install -r requirements.txt
3. 修改相关配置如数据库配置等
4. 执行数据库迁移 python manage.py makemigrations
5. python manage.py migrate               
6. 创建superuser python manage.py createsuperuser
7. 执行python manage.py runserver 

##通过Docker
1. 这里假定已经启动了mysql服务的容器
2. 构建镜像docker build --tag xx --rm=true .
3. 启动容器docker run --name XXX -d -p 8000:8000 --link mysql:mysql -v /var/run/docker.sock:/var/run/docker.sock XX
