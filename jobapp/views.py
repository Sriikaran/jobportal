from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Login, Employer, JobSeeker, Enquiry
from adminapp.models import News
from employer.models import Jobs
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
import datetime
from django.db.models import Q
from django.contrib import messages

def index(request):
    jobs = Jobs.objects.all()
    q = request.GET.get('q')
    if q:
        jobs = jobs.filter(
            Q(post__icontains=q) |
            Q(location__icontains=q) |
            Q(jobdesc__icontains=q) |
            Q(firmname__icontains=q) |
            Q(qualification__icontains=q)
        )
        jobs = list(jobs)  # Force evaluation
        print(f"Search query: {q}, Found jobs: {len(jobs)}, Jobs: {[job.post for job in jobs]}")
    else:
        print(f"No search query, Total jobs: {jobs.count()}")
    context = {'jobs': jobs, 'q': q}
    print("Context:", context)
    return render(request, "index.html", context)

def search_jobs(request):
    jobs = Jobs.objects.all()
    q = request.GET.get('q')
    if q:
        jobs = jobs.filter(
            Q(post__icontains=q) |
            Q(location__icontains=q) |
            Q(jobdesc__icontains=q) |
            Q(firmname__icontains=q) |
            Q(qualification__icontains=q)
        )
    job_list = [{
        'post': job.post,
        'location': job.location,
        'posteddate': job.posteddate,  # Use string directly
        'jobtitle': job.jobtitle,
        'firmname': job.firmname,
        'qualification': job.qualification,
        'jobdesc': job.jobdesc,
        'salarypa': str(job.salarypa),
        'emailaddress': job.emailaddress
    } for job in jobs]
    return JsonResponse({'jobs': job_list})

def aboutus(request):
    return render(request, "aboutus.html")

def jobseekerreg(request):
    if request.method == "POST":
        profilepic = request.POST["profilepic"]
        name = request.POST["name"]
        gender = request.POST["gender"]
        address = request.POST["address"]
        contactno = request.POST["contactno"]
        emailaddress = request.POST["emailaddress"]
        password = request.POST["password"]
        dob = request.POST["dob"]
        regdate = datetime.datetime.today()

        jobseek = JobSeeker(
            profilepic=profilepic,
            name=name,
            gender=gender,
            address=address,
            contactno=contactno,
            emailaddress=emailaddress,
            dob=dob,
            regdate=regdate
        )
        jobseek.save()

        log = Login(username=emailaddress, password=password, usertype="jobseeker")
        log.save()

        messages.success(request, "Registration successful! You can now log in.")
        return render(request, "jobseeker.html", {"show_modal": True})

    return render(request, "jobseeker.html")

from django.contrib import messages
from jobapp.models import Employer, Login
import datetime

def employerreg(request):
    if request.method == "POST":
        empprofilepic = request.FILES.get("empprofilepic")
        firmname = request.POST["firmname"]
        firmwork = request.POST["firmwork"]
        firmaddress = request.POST["firmaddress"]
        cpname = request.POST["cpname"]
        cpcontactno = request.POST["cpcontactno"]
        cpemailaddress = request.POST["cpemailaddress"]
        password = request.POST["password"]
        aadharno = request.POST["aadharno"]
        panno = request.POST["panno"]
        gstno = request.POST["gstno"]
        regdate = datetime.datetime.today()

        empreg = Employer(
            empprofilepic=empprofilepic,
            firmname=firmname,
            firmwork=firmwork,
            firmaddress=firmaddress,
            cpname=cpname,
            cpcontactno=cpcontactno,
            cpemailaddress=cpemailaddress,
            aadharno=aadharno,
            panno=panno,
            gstno=gstno,
            regdate=regdate
        )
        empreg.save()

        Login.objects.create(username=cpemailaddress, password=password, usertype="employer")

        # 🔹 Set session for auto-login
        request.session["username"] = cpemailaddress
        request.session["usertype"] = "employer"

        messages.success(request, "Employer registration successful! You are now logged in.")
        return redirect("employer:employerhome")  # ✅ Go straight to employer home

    return render(request, "employer.html")



def login(request):
    print("AFTER LOGIN:", username, obj.usertype)
    print("SESSION NOW:", dict(request.session))

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            obj = Login.objects.get(username=username, password=password)
            request.session["username"] = username
            request.session["usertype"] = obj.usertype 
            print("SESSION:", request.session.items())
 

            if obj.usertype == 'jobseeker':
                return redirect("jsapp:jshome")
            elif obj.usertype == 'administrator':
                return redirect("adminapp:adminhome")
            elif obj.usertype == 'employer':
                return redirect("employer:employerhome")
            else:
                return render(request, 'login.html', {"msg": "Invalid user type"})

        except Login.DoesNotExist:
            return render(request, 'login.html', {"msg": "Invalid username or password"})

    return render(request, "login.html")



def contactus(request):
    if request.method=="POST": 
        name=request.POST["name"] 
        gender=request.POST["gender"]
        address=request.POST["address"]
        contactno=request.POST["contactno"]
        emailaddress=request.POST["emailaddress"]
        enquirytext=request.POST["enquirytext"]
        posteddate=datetime.datetime.today()
        enq=Enquiry(name=name, gender=gender, address=address, contactno=contactno, emailaddress=emailaddress, enquirytext=enquirytext, posteddate=posteddate)
        enq.save()
        return render(request, "contactus.html", {"msg": "Enquiry is saved"})
    return render(request, "contactus.html")

def apply(request):
    return render(request, "apply.html")

def services(request):
    return render(request, "services.html")

def blog(request):
    new = News.objects.all()
    return render(request, "blog.html", locals())

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = Login.objects.get(username=email)
            return render(request, 'reset_password.html', {'user_email': user.username})
        except Login.DoesNotExist:
            messages.error(request, "Email not registered.")
    return render(request, 'forgot_password.html')