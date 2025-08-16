from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

# Avoid storing passwords in plain text!
# If you're not using Django's built-in auth system, hash passwords before saving!

class Login(models.Model):
    username = models.CharField(max_length=50, primary_key=True)
    password = models.CharField(max_length=128)  # Increased length for hashed passwords
    usertype = models.CharField(max_length=50)

    def __str__(self):
        return self.username


class Enquiry(models.Model):
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=6, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    address = models.CharField(max_length=100)  # TextField doesn't support max_length, use CharField
    contactno = models.CharField(max_length=15)
    emailaddress = models.EmailField(max_length=50)
    enquirytext = models.TextField()
    posteddate = models.DateField()  # Prefer DateField for dates

    def __str__(self):
        return f"{self.name} - {self.emailaddress}"


class JobSeeker(models.Model):
    profilepic = models.ImageField(upload_to='jobseekers/', default='pic')  # FileField -> ImageField + folder
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=6, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    address = models.TextField()
    contactno = models.CharField(max_length=15)
    emailaddress = models.EmailField(max_length=50, primary_key=True)
    dob = models.DateField()
    qualification = models.CharField(max_length=100)
    experience = models.CharField(max_length=20)
    keyskills = models.TextField()
    regdate = models.DateField()

    def __str__(self):
        return self.emailaddress


class Employer(models.Model):
    empprofilepic = models.ImageField(upload_to='employers/', default='pic')
    firmname = models.CharField(max_length=100)
    firmwork = models.TextField()
    firmaddress = models.TextField()
    cpname = models.CharField(max_length=50)
    cpcontactno = models.CharField(max_length=15)
    cpemailaddress = models.EmailField(max_length=50, primary_key=True)
    aadharno = models.CharField(max_length=12)
    panno = models.CharField(max_length=10)
    gstno = models.CharField(max_length=15)
    regdate = models.DateField()

    def __str__(self):
        return self.firmname
    

class Administrator(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer not to say'),
    ]
    
    DEPARTMENT_CHOICES = [
        ('hr', 'Human Resources'),
        ('it', 'Information Technology'),
        ('finance', 'Finance'),
        ('operations', 'Operations'),
        ('management', 'Management'),
    ]
    
    ACCESS_LEVEL_CHOICES = [
        ('super_admin', 'Super Administrator'),
        ('admin', 'Administrator'),
        ('moderator', 'Moderator'),
    ]
    
    # Basic Information
    profilepic = models.ImageField(upload_to='admin_profiles/', null=False, blank=False)
    fullName = models.CharField(max_length=100, null=False, blank=False)
    username = models.CharField(max_length=50, unique=True, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    
    # Phone number validation
    phone_regex = RegexValidator(
        regex=r'^\+?\d{10,15}',
        message="Phone number must be entered in the format: '+1234567890'. Up to 15 digits allowed."
    )
    phone = models.CharField(validators=[phone_regex], max_length=17, null=False, blank=False)
    
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=False, blank=False)
    dob = models.DateField(null=False, blank=False)
    
    # Address Information
    address = models.TextField(null=False, blank=False)
    city = models.CharField(max_length=50, null=False, blank=False)
    state = models.CharField(max_length=50, null=False, blank=False)
    country = models.CharField(max_length=50, default='India', null=False, blank=False)
    
    # Admin Specific Fields
    employeeId = models.CharField(max_length=20, unique=True, null=False, blank=False)
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES, null=False, blank=False)
    accessLevel = models.CharField(max_length=20, choices=ACCESS_LEVEL_CHOICES, null=False, blank=False)
    
    # System Fields
    regdate = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'administrator'
        verbose_name = 'Administrator'
        verbose_name_plural = 'Administrators'
        ordering = ['-regdate']
    
    def __str__(self):
        return f"{self.fullName} ({self.username})"
    
    def get_full_name(self):
        return self.fullName
    
    def get_department_display_name(self):
        return dict(self.DEPARTMENT_CHOICES)[self.department]
    
    def get_access_level_display_name(self):
        return dict(self.ACCESS_LEVEL_CHOICES)[self.accessLevel]

