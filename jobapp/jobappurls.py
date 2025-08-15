from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views  # ✅ This must be included once

urlpatterns = [
    path('', views.index, name="index"),
    path('search-jobs/', views.search_jobs, name='search_jobs'),
    path('aboutus/', views.aboutus, name="aboutus"),
    path('services/', views.services, name="services"),
    path('blog/', views.blog, name="blog"),
    path('contactus/', views.contactus, name="contactus"),
    path('login/', views.login, name="login"),
    path('apply/', views.apply, name="apply"),
    path('jobseekerreg/', views.jobseekerreg, name="jobseekerreg"),
    path('employerreg/', views.employerreg, name="employerreg"),
    
    # ✅ Password reset URLs
    path('forgot-password/', auth_views.PasswordResetView.as_view(), name='forgot_password'),
    path('forgot-password/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
