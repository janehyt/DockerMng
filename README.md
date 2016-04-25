MyWeb
=====
1. 首先安装node（>4.2）
2. 再全局安装gulp npm install --global gulp
3. 在webapp目录下执行gulp
4. 建立virtualenv环境
5. 进入独立python环境后执行pip install -r requirements.txt
6. 修改相关配置如数据库配置等
7. 执行数据库迁移 python manage.py makemigrations
               python manage.py migrate
8. 创建superuser python manage.py createsuperuser
9. 执行python manage.py runserver 
