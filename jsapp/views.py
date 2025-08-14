from django.shortcuts import render, redirect
from employer.models import Jobs, Post
from jsapp.models import Response, SavedJob
from django.contrib import messages
from jobapp.models import JobSeeker,Employer, Login
from .models import AppliedJobs
import datetime
from django.shortcuts import get_object_or_404

def index(request):
    return render(request, "index.html")

def aboutus(request):
    return render(request, "aboutus.html")

def contactus(request):
    return render(request, "contactus.html")

def services(request):
    return render(request, "services.html")

def blog(request):
    return render(request, "blog.html")

def login(request):
    if request.session.pop('password_changed', False):
        messages.success(request, "Password changed successfully. Please log in again.")
    return render(request, "login.html")

def employer(request):
    if request.method == "POST":
        companyname = request.POST.get("companyname")
        emailaddress = request.POST.get("emailaddress")
        password = request.POST.get("password")
        Employer(companyname=companyname, emailaddress=emailaddress, password=password).save()
        messages.success(request, "Employer account created successfully.")
        return redirect('login')
    return render(request, "employer.html")

def appliedjobs(request):
    if "username" not in request.session:
        return redirect("login")

    seeker_email = request.session["username"]
    jobseeker = JobSeeker.objects.get(emailaddress = seeker_email)
    jobs = AppliedJobs.objects.filter(emailaddress=seeker_email)

    return render(request, "appliedjobs.html", {"jobs": jobs,"jobseek": jobseeker})

def viewprofile(request):
    if "username" not in request.session:
        return redirect("login")


    seeker_email = request.session["username"]

    if request.method == "POST":
        jobseeker = JobSeeker.objects.get(emailaddress = seeker_email)
        profile_pic = request.FILES.get("profilepic")
        if profile_pic:
            jobseeker.profilepic = profile_pic
        jobseeker.name= request.POST.get("name")
        jobseeker.gender = request.POST.get("gender")
        jobseeker.address = request.POST.get('address')
        jobseeker.contactno = request.POST.get('contactno')
        dob_str = request.POST.get("dob")
        if dob_str:
            try:
                jobseeker.dob = datetime.datetime.strptime(dob_str, "%Y-%m-%d").date()
            except ValueError:
                messages.error(request, "Invalid date format for DOB. Use YYYY-MM-DD.")
        
        jobseeker.qualification  = request.POST.get('qualification')
        jobseeker.experience = request.POST.get('experience')
        jobseeker.keyskills = request.POST.get('keyskills')
        jobseeker.save()
        messages.success(request, "Profile updated")

    try:
        jobseeker = JobSeeker.objects.get(emailaddress=seeker_email)
    except JobSeeker.DoesNotExist:
        jobseeker = None

    return render(request, "viewprofile.html", {"jobseek": jobseeker})

def response(request):
    if "username" not in request.session:
        return redirect("login")

    email = request.session["username"]
    jobseeker = JobSeeker.objects.get(emailaddress = email)
    responses = Response.objects.filter(emailaddress=email).order_by("-posteddate")

    return render(request, "response.html", {"responses": responses,"jobseek": jobseeker})

def jobseeker(request):
    if request.method == "POST":
        name = request.POST.get("name")
        emailaddress = request.POST.get("emailaddress")
        password = request.POST.get("password")
        Response(name=name, emailaddress=emailaddress, password=password).save()
        messages.success(request, "Job Seeker account created successfully.")
        return redirect('login')
    return render(request, "jobseeker.html")

def apply(request, jobid):
    if "username" not in request.session:
        return redirect("login")
    
    job = get_object_or_404(Jobs, id=jobid)
    
    if request.method == "POST":
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        resume = request.FILES.get("resume")
        
        Response(job=job, fullname=fullname, email=email, phone=phone, resume=resume).save()
        messages.success(request, "Application submitted successfully.")
        return redirect("index")
    
    return render(request, "apply.html", {"job": job})

def parent(request):
    return render(request, "parent.html")

def admin_dashboard(request):
    jobs = Jobs.objects.all()
    return render(request, "admin.html", {"jobs": jobs})

def applyjob(request, jobid):
    if "username" not in request.session:
        return redirect("login")
    
    job = Jobs.objects.get(id=jobid)
    return render(request, "apply.html", {"job": job})

def myapplications(request):
    if "username" not in request.session:
        return redirect("login")
    
    email = request.session["username"]
    applications = Response.objects.filter(emailaddress=email)
    return render(request, "myapplications.html", {"applications": applications})

def logout(request):
    try:
        del request.session["username"]
    except:
        pass
    return redirect("index")
def changepassword(request):
    if "username" not in request.session:
        return redirect("jobapp:login")

    if request.method == "POST":
        current_password = request.POST.get("oldpassword")
        new_password = request.POST.get("newpassword")
        confirm_password = request.POST.get("cnfpassword")
        email = request.session["username"]

        try:
            user = Login.objects.get(username=email)

            if user.password != current_password:
                messages.error(request, "Current password is incorrect.")
                return redirect("jsapp:changepassword")

            if new_password != confirm_password:
                messages.error(request, "New password & confirm password do not match.")
                return redirect("jsapp:changepassword")

            user.password = new_password
            user.save()
            
            request.session['password_changed'] = True
            return redirect("jobapp:login")

        except Login.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect("jobapp:login")

    return render(request, "changepassword.html")
# NEW FEATURE: Save Job
def savejob(request, jobid):
    if "username" not in request.session:
        return redirect("login")
    
    job = Jobs.objects.get(id=jobid)
    user_email = request.session["username"]

    # Check if already saved
    if not SavedJob.objects.filter(user_email=user_email, job=job).exists():
        SavedJob.objects.create(user_email=user_email, job=job)
        messages.success(request, "Job saved successfully.")
    else:
        messages.info(request, "You already saved this job.")
    
    return redirect("index")

def jsapply(request, id):
    if "username" not in request.session:
        return redirect("login")

    job = get_object_or_404(Jobs, id=id)
    seeker = get_object_or_404(JobSeeker, emailaddress=request.session['username'])

    if request.method == "POST":
        AppliedJobs.objects.create(
            empemailaddress=job.emailaddress,
            jobtitle=job.jobtitle,
            post=job.post,
            name=seeker.name,
            gender=seeker.gender,
            address=seeker.address,
            contactno=seeker.contactno,
            emailaddress=seeker.emailaddress,
            dob=seeker.dob,
            qualification=seeker.qualification,
            experience=seeker.experience,
            keyskills=seeker.keyskills,
            applieddate=datetime.now().strftime("%Y-%m-%d"),
        )
        return render(request, "applied_success.html", {"job": job})

    return render(request, "applyjob.html", {"job": job, "seeker": seeker})

def jshome(request):
    # return render(request, 'jshome.html')  # create jsapp/templates/jsapp/home.html if needed

    if request.session.get("usertype") != "jobseeker":
        return redirect("jobapp:login")
    seeker_email = request.session.get("username")
    jobseeker = JobSeeker.objects.get(emailaddress = seeker_email)
 
    return render(request, 'jshome.html',{"jobseek": jobseeker})




def viewjobs(request):
    # Just rendering a template for now
    return render(request, 'viewjobs.html')
def logout(request):
    try:
        del request.session["username"]
    except KeyError:
        return redirect("jobapp:login")
    return redirect("jobapp:login")
# def jshome(request):
#     if request.session.get("usertype") != "jobseeker":
#         return redirect("jobapp:login")
#     return render(request, 'jshome.html')
