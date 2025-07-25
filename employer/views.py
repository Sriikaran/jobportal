from django.shortcuts import render,redirect
from jobapp.models import Employer,JobSeeker,Tags
from . models import Jobs,Post
from django.views.decorators.cache import cache_control
import datetime
from jsapp.models import AppliedJobs
# Create your views here.
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def employerhome(request):
    try:
        if request.session["username"]!=None:
            username=request.session["username"]
            empreg=Employer.objects.get(cpemailaddress=username)
            return render(request,"employerhome.html",locals())
    except KeyError:
        return redirect("employer:login")
def logout(request):
    try:
        del request.session["username"]
    except KeyError:
        return redirect("jobapp:login")
    return redirect("jobapp:login")
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def jobs(request):
    try:
        if request.session["username"]!=None:
            username=request.session["username"]
            empreg=Employer.objects.get(cpemailaddress=username)
            if request.method=="POST":
                firmname=request.POST['firmname']
                jobtitle=request.POST['jobtitle']
                post=request.POST['post']
                jobdesc=request.POST['jobdesc']
                qualification=request.POST['qualification']
                experience=request.POST['experience']
                location=request.POST['location']
                salarypa=request.POST['salarypa']
                tags=request.POST['tagname']
                clean_tags = tags.split(",")
                posteddate=datetime.datetime.today()
                emailaddress=request.POST['emailaddress']
                pjobs=Jobs(firmname=firmname,jobtitle=jobtitle,post=post,jobdesc=jobdesc,qualification=qualification,experience=experience,location=location,salarypa=salarypa,posteddate=posteddate,emailaddress=emailaddress)
                pjobs.save()
                for t in  clean_tags:
                      t=t.lower()
                      t_obj,created= Tags.objects.get_or_create(tag_name=t)
                      pjobs.job_tags.add(t_obj)
                msg="Job Post is added"
                return render(request,"jobs.html",locals())
            return render(request,"jobs.html",locals())
    except KeyError:
        return redirect("jobapp:login")

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def postedjobs(request):
    try:
        if request.session["username"]!=None:
            username=request.session["username"]
            pjobs=Jobs.objects.filter(emailaddress=username)
            emp=Employer.objects.all()
        return render(request,"postedjobs.html",locals())
    except KeyError:
        return redirect("jobapp:login")
def deljob(request,post):
    Jobs.objects.get(post=post).delete()
    return redirect("employer:postedjobs")
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def discussion(request):
    try:
        if request.session["username"]!=None:
            username=request.session["username"]
            return render(request,"discussion.html",locals())
    except KeyError:
        return redirect("employer:login")
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def viewapplicants(request):
    try:
        if request.session["username"]!=None:
            username=request.session["username"]
            post=AppliedJobs.objects.filter(emailaddress=username)
            return render(request,"viewapplicants.html",locals())
    except KeyError:
        return redirect("jobapp:login")
def reject(request,emailaddress):
    AppliedJobs.objects.get(emailaddress=emailaddress).delete()
    return redirect("employer:viewapplicants")
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def viewmyprofile(request):
    try:
        if request.session["username"]!=None:
            username=request.session["username"]
            empreg=Employer.objects.get(cpemailaddress=username)
            if request.method=="POST":
                firmname=request.POST["firmname"]
                firmwork=request.POST["firmwork"]
                firmaddress=request.POST["firmaddress"]
                cpname=request.POST["cpname"]
                cpcontactno=request.POST["cpcontactno"]
                cpemailaddress=request.POST["cpemailaddress"]
                Employer.objects.all(cpemailaddress=cpemailaddress).update(firmname=firmname,firmwork=firmwork,firmaddress=firmaddress,cpname=cpname,cpcontactno=cpcontactno)
                return redirect("employer:employerhome",locals())
            return render(request,"viewmyprofile.html",locals())
    except KeyError:
        return redirect("jobapp:login")
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def addpost(request):
    try:
        if request.session["username"]!=None:
            username=request.session["username"]
            empreg=Employer.objects.get(cpemailaddress=username)
            if request.method=="POST":
                cpname=request.POST['cpname']
                cpemailaddress=request.POST['cpemailaddress']
                caption=request.POST['caption']
                media=request.FILES['media']
                posteddate=datetime.datetime.today()
                apost=Post(cpname=cpname,cpemailaddress=cpemailaddress,caption=caption,media=media,posteddate=posteddate)
                apost.save()
                msg="Post is added"
                return render(request,"addpost.html",locals())
            return render(request,"addpost.html",locals())
    except KeyError:
        return redirect("jobapp:login")

