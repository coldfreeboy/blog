from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^home/$',views.home,name="home"),
    url(r'^(?P<tag>(log_in|log_up))/$',views.login,name="login"),
]
