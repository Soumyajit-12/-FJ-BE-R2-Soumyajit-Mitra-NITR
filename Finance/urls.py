"""Finance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from Tracker import views as t_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    # path('register/', t_views.register , name='register'),
    path('', t_views.index , name='index'),
    path('signup/', t_views.signup , name='signup'),
    path('home/', t_views.home , name='home'),
    path('form/', t_views.form , name='form'),
    path('delete/<id>/', t_views.delete , name='delete'),
    path('logout/', t_views.logout_view, name="logout"),
    path('api/records/', t_views.api_records_list, name='api_records_list'),
]
