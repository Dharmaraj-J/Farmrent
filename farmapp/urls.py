from django.urls import path
from . import views

urlpatterns = [
     path('',views.indexpage,name='indexpage'),

    path('loginpage/',views.loginpage,name='loginpage'),
    path('handellogin',views.handellogin, name='handellogin'),

    path('registerpage/',views.registerpage,name='registerpage'),
    path('handleregister',views.handleregister, name='handleregister'),

    
    path('customerpage/',views.customerpage,name='customerpage'),
    path('rentalmanagerpage/',views.rentalmanagerpage,name='rentalmanagerpage'),


    path('handlelogout/',views.handlelogout, name='handlelogout'), 

    path('addequipment',views.addequipment, name='addequipment'),
    path('add',views.add, name='add'),

    path('editequipment',views.editequipment, name='editequipment') ,
    path('edit/<str:slug>',views.edit, name='edit'),
    path('delete/<str:slug>',views.delete, name='delete'),
  

    path('equipmentdetail/<int:equipment_id>/', views.equipmentdetail, name='equipmentdetail'),

    path('apply/<str:slug>',views.apply, name='apply'),

    path('requests',views.requests, name='requests'),
    path('denied_request/<str:slug>',views.denied_request, name='denied_request'),
    path('accept_request/<str:slug>',views.accept_request,name='accept_request'),

    path('searchpage',views.searchpage,name="searchpage"),

]