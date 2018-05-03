from django.conf.urls import url
from job import views

urlpatterns = [
    url(r'^run/$', views.RunScript.as_view()),
]