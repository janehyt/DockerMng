"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.views.static import serve
from rest_framework import routers
from api import views
from mysite import settings as settings
from django.http import HttpResponseRedirect as HttpResponseRedirect


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    url(r'^$',serve, 
        {'document_root': settings.DIST_PATH,
        'path':'index.html'}),
	url(r'^api/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^(?P<path>(?:js|css|img|fonts|img|l10n|tpl|vendor)/.*)$', serve,{'document_root': settings.DIST_PATH}),
]

def page_not_found(request):
    return HttpResponseRedirect('/#/access/404')


handler404 = page_not_found

# handler500 = page_not_found
# if settings.DEBUG:
#     from django.views.static import serve
#     urlpatterns += [
#         url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_PATH}),
#         # url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], serve, {'document_root': settings.MEDIA_ROOT}),
#     ]
