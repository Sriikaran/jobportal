from django.urls import path
from . import views

app_name = 'adminapp'

urlpatterns=[
    path("test/", views.test_template, name="test_template"),
    path('adminhome/',views.adminhome,name='adminhome'),
    path('news/',views.news,name='news'),
    path('delnews/<newsdate>',views.delnews,name='delnews'),
    path('viewnews/',views.viewnews,name='viewnews'),
    path('logout/',views.logout,name='logout'),
    path('viewenquiries/',views.viewenquiries,name='viewenquiries'),
    path('viewfeedback/',views.viewfeedback,name='viewfeedback'),
    path('viewcomplaints/',views.viewcomplaints,name='viewcomplaints'),
    path('viewemployers/',views.viewemployers,name='viewemployers'),
    path('viewjobseekers/',views.viewjobseekers,name='viewjobseekers'),
    path('delenq/<emailaddress>',views.delenq,name="delenq"),
]