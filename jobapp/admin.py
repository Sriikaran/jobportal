from django.contrib import admin
from . models import Enquiry,JobSeeker,Employer,Login, Administrator
# Register your models here.
admin.site.register(Enquiry)
admin.site.register(Employer)
admin.site.register(JobSeeker)
admin.site.register(Administrator)
admin.site.register(Login)