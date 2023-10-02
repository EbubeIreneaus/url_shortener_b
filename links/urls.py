
from django.urls import path
from . import views

urlpatterns = [
	path('', views.Isllinks.as_view()),

]