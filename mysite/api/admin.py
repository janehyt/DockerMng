# -*- coding: UTF-8 -*-
'''admin'''
from django.contrib import admin
from .models import Volume, Repository, Image, Process,\
Container, Link, Bind, Port, Environment, Creation
# Register your models here.
admin.site.register(Volume)
admin.site.register(Repository)
admin.site.register(Image)
admin.site.register(Process)
admin.site.register(Container)
admin.site.register(Link)
admin.site.register(Bind)
admin.site.register(Port)
admin.site.register(Environment)
admin.site.register(Creation)
