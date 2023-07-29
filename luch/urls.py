"""
URL configuration for luch project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from gsadashboard import views


urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('saveUser/', views.saveUserData, name='saveUser'),
    path('savePass/', views.savePassword, name='savePassword'),
    path('admin/', admin.site.urls),
    path('sync/', views.sync_rfq, name='sync'),
    path('list_rfqs/', views.rfqList, name='listRfqs'),
    path('keywords/', views.listKeywords, name='keywords'),
    path('keywords/create/', views.createKeywords, name='keywords_create'),
    path('rfq_view/<int:id>', views.rfqView,name="refqView"),
    path('keywords/delete/<int:id>', views.deleteKeywords,name="deleteKey"),
    path('keywords/edit/<int:id>', views.editKeywords,name="editKey"),
    path('sigin/', views.signin,name="signin"),
    path('token/', views.saveToken,name="token"),
    path('signup/', views.signup,name="signup"),
    path('logout/', views.signout, name='logout'),
]

