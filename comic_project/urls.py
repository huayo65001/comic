"""comic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.start,name='start'),
    path('index/', views.index,name='index'),
    path('all/',views.all,name='all'),
    path('home/',views.home,name='home'),
    path('profile/',views.profile,name='profile'),
    path('comic_content/',views.comic_content,name='comic_content'),
    path('comic_rank/',views.comic_rank,name='comic_rank'),
    path('comic_detail/',views.comic_detail,name='comic_detail'),
    path('comic_final/',views.comic_final,name='comic_final'),
    path('login/',views.login,name='login'),
    path('login_valid/',views.login_valid,name='login_valid'),
    path('login_render/',views.login_render,name='login_render'),
    path('register/',views.register,name='register'),
    path('register_valid/',views.register_valid,name='register_valid'),
    path('forget/',views.forget,name='forget'),
    path('logout/',views.logout,name='logout'),
    path('search/',views.search,name='search'),
    path('addfoucs/',views.addfoucs,name='addfoucs'),
    path('removefoucs/',views.removefoucs,name='removefoucs'),
    path('form_v/',views.form_v,name='form_v'),
    path('form_valid/',views.form_valid,name='form_valid'),
    path('change/',views.change,name='change'),
    path('delete_user/',views.delete_user,name='delete_user'),
    path('form_c/',views.form_c,name='form_c'),
    path('form_change/',views.form_change,name='form_change')
]+ static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
