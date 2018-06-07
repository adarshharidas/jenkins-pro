from django.conf.urls import url
from job import views

urlpatterns = [
    url(r'^', views.RunScript.as_view()),
]