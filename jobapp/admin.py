from django.contrib import admin
from . models import Enquiry,JobSeeker,Employer,Login
# Register your models here.
admin.site.register(Enquiry)
admin.site.register(Employer)
admin.site.register(JobSeeker)
admin.site.register(Login)