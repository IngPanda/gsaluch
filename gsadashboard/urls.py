from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sync/', views.sync_rfq, name='sync'),
    path('list_rfqs/', views.rfqList, name='listRfqs'),
    path('rfq-view/<int:id>', views.rfqView,name="refqView"),
    path('sigin/', views.signin,name="signin"),
    path('signup/', views.signup,name="signup"),
    path('logout/', views.signout, name='logout'),
]