from django.urls import path
from . import views

app_name = 'employer'

urlpatterns=[
    #path("test/", views.test_template, name="test_template"),
    path('employerhome/',views.employerhome,name='employerhome'),
    path('employer/', views.employerhome, name='employer'),
    path('jobs/',views.jobs,name='jobs'),
    path('postedjobs/',views.postedjobs,name='postedjobs'),
    path('deljob/<post>',views.deljob,name='deljob'),
    path('reject/<emailaddress>',views.reject,name='reject'),
    path('viewapplicants/',views.viewapplicants,name='viewapplicants'),
    path('viewmyprofile/',views.viewmyprofile,name='viewmyprofile'),
    path('logout/',views.logout,name='logout'),
    path('addpost/',views.addpost,name='addpost'),
    path('viewpjobs/', views.viewpjobs, name='viewpjobs'),
    # path('forgot-password/', views.forgot_password, name='forgot_password')
]