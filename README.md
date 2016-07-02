DockerMng 安装
=====
# 安装docker
* 请参见 [docker官方说明文档](https://docs.docker.com/engine/installation/)

# 拉取仓库内容

# 构建前端页面
* 首先安装node（>4.2）
* 再全局安装gulp npm install --global gulp
* 在webapp目录下执行gulp

# 准备数据库
* 导入数据库 dockermng.sql（若不导入，也可在后台中通过django进行数据库迁移）

# 启动后台(在mysite文件夹下)，基于python
1. 通过docker启动django
* 假定已配置好mysql服务器
* 构建镜像 `docker build --tag xx --rm=true .`
* 启动容器 `docker run --name XXX -d -p 8000:8000 --link mysql:mysql -v /var/run/docker.sock:/var/run/docker.sock XX`
2. 直接启动
* 安装依赖`pip install -r requirements.txt`
* 修改相关配置如数据库配置等
* 如果是导入数据库，则默认用户名为admin，密码为123456
* 执行 `python manage.py runserver` 启动服务器
