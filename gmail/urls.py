from django.urls import path
from gmail import views


urlpatterns=[
    path('',views.index,name='index'),
    path('home',views.home,name='home'),
    path('logout',views.logout,name='logout'),
    path('send',views.send_mail,name='send_mail'),
    path('receive',views.receive_mail,name='receive_mail'),
    path('delete',views.delete_mail,name='delete_mail')
]
