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
from gsadashboard.controllers import rfq_controller, vendor_controller, access_controller, user_controller, keywords_controller, comment_controller


urlpatterns = [
    # Dashboard
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),


    # RFQ
    path('sync/', rfq_controller.sync_rfq, name='sync'),
    path('list_rfqs/',rfq_controller.rfqList, name='listRfqs'),
    path('rfq_view/<int:id>', rfq_controller.rfqView,name="refqView"),

    # Profile
    
    path('profile/', user_controller.profile, name='profile'),
    path('saveUser/', user_controller.saveUserData, name='saveUser'),
    path('savePass/', user_controller.savePassword, name='savePassword'),
    path('admin/', admin.site.urls),

    # Keywords
    path('keywords/', keywords_controller.listKeywords, name='keywords'),
    path('keywords/create/', keywords_controller.createKeywords, name='keywords_create'),
    path('keywords/delete/<int:id>', keywords_controller.deleteKeywords,name="deleteKey"),
    path('keywords/edit/<int:id>', keywords_controller.editKeywords,name="editKey"),
    path('keywords/edit/<int:id>/<str:state>', keywords_controller.editKeywordsState,name="editKey"),

    # Vendors
    path('vendors/<int:cat>', vendor_controller.vendorList,name="vendorsList"),
    
    #access user
    
    path('sigin/', access_controller.signin,name="signin"),
    path('token/', views.saveToken,name="token"),
    path('signup/', access_controller.signup,name="signup"),
    path('logout/', access_controller.signout, name='logout'),

    #comment
    path('comment/', comment_controller.saveComment,name="createComment")

]

