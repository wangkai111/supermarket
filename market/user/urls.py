from django.conf.urls import url

from user.views import login

urlpatterns = [
    url(r'^$',login,name="登录"),
]