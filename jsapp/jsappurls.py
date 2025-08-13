from django.urls import path
from . import views

app_name = 'jsapp'

urlpatterns=[
    path('jsapp/',views.jshome,name='jshome'),
    path('viewjobs/',views.viewjobs,name='viewjobs'),
    path('logout/',views.logout,name='logout'),
    path('changepassword/',views.changepassword,name='changepassword'),
    path('jsapply/',views.jsapply,name='jsapply'),
    path('appliedjobs/',views.appliedjobs,name='appliedjobs'),
    path('viewprofile/',views.viewprofile,name='viewprofile'),
    path('response/',views.response,name='response'),

]

