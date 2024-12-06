"""
URL configuration for to_do project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from to_do_list.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name="loginview"),
    path('signup/', SignUpView.as_view(), name="signupview"),
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
    path('todoadd/', TodoView.as_view(), name="todoadd"),
    path('todolist/', TodolistView.as_view(), name="todolist"),
    path('taskdisplays/<int:task_id>/', TaskView.as_view(), name="taskdisplays"),
    path('deletetask/<int:task_id>/', DeleteTaskView.as_view(), name='deletetask'),
    path('taskedit/<int:task_id>/',EditTaskView.as_view(), name="taskedit"),
    path('completelist/', CompletelistView.as_view(), name="completelist"),
    path('profile/', ProfileView.as_view(), name="profile"),
]
