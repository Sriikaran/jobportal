from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name="index"),
    path('aboutus/',views.aboutus,name="aboutus"),
    path('services/',views.services,name="services"),
    path('blog/',views.blog,name="blog"),
    path('contactus/',views.contactus,name="contactus"),
    path('login/',views.login,name="login"),
    path('apply/',views.apply,name="apply"),
    path('jobseekerreg/',views.jobseekerreg,name="jobseekerreg"),
    path('employerreg/',views.employerreg,name="employerreg"),
    ]
