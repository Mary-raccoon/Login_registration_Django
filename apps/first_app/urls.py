from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
    url(r'^$', views.index),
    url(r'^process$', views.process),
    url(r'^login$', views.login),
    url(r'^quotes$', views.quotes),
    url(r'^create_process$', views.create_process),
    url(r'^favorite_quote/(?P<id>\d+)$', views.favorite_quote),
    url(r'^remove_quote/(?P<id>\d+)$', views.remove_quote),
    url(r'^logout$', views.logout),
    url(r'^users/(?P<id>\d+)$', views.users),
]