from django.shortcuts import render,redirect
from jobapp.models import JobSeeker,Employer
from django.views.decorators.cache import cache_control
from employer.models import Jobs,Post
import datetime
from . models import AppliedJobs,Response
# Create your views here.
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def jshome(request):
    try:
        if request.session["username"]!=None:
            username=request.session["username"]
            empreg=Employer.objects.all()
            jobseek=JobSeeker.objects.get(emailaddress=username)
            job=Jobs.objects.all()
            apost=Post.objects.all()
            return render(request,"jshome.html",locals())
    except KeyError:
        return redirect("jobapp:login")
def logout(request):
    try:
        del request.session["username"]
    except KeyError:
        return redirect("jobapp:login")
    return redirect("jobapp:login")
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def viewjobs(request):
    try:
        if request.session["username"]!=None:
            username=request.session["username"]
            jobseek=JobSeeker.objects.get(emailaddress=username)
            pjobs=Jobs.objects.all()
            return render(request,"viewjobs.html",locals())
    except KeyError:
        return redirect("jobapp:login")
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def viewprofile(request):
    #try:
        if request.session["username"]!=None:
            username=request.session["username"]
            jobseek=JobSeeker.objects.get(emailaddress=username)
            if request.method=="POST":
                name=request.POST["name"]
                gender=request.POST["gender"]
                address=request.POST["address"]
                contactno=request.POST["contactno"]
                emailaddress=request.POST["emailaddress"]
                qualification=request.POST["qualification"]
                dob=request.POST["dob"]
                experience=request.POST["experience"]
                keyskills=request.POST["keyskills"]
                JobSeeker.object.all()
                return redirect("jsapp:jshome",locals())
            return render(request,"viewprofile.html",locals())
    #except KeyError:
        #return redirect("jobapp:login")
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def changepassword(request):
    try:
        if request.session["username"]!=None:
            username=request.session["username"]
            return render(request,"changepassword.html",locals())
    except KeyError:
        return redirect("jobapp:login")
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def jsapply(request,id):
    try:
        if request.session["username"]!=None:
            username=request.session["username"]
            job=Jobs.objects.get(id=id)
            jobseek=JobSeeker.objects.get(emailaddress=username)
            if request.method=="POST": 
                empemailaddress=request.POST["empemailaddress"] 
                jobtitle=request.POST["jobtitle"]
                post=request.POST['post']
                name=request.POST['name']
                gender=request.POST['gender']
                address=request.POST["address"]
                contactno=request.POST["contactno"]
                emailaddress=request.POST["emailaddress"]
                dob=request.POST["dob"]
                qualification=request.POST["qualification"]
                experience=request.POST["experience"]
                keyskills=request.POST["keyskills"]
                applieddate=datetime.datetime.today()
                app=AppliedJobs(empemailaddress=empemailaddress,jobtitle=jobtitle,post=post,name=name,gender=gender,address=address,contactno=contactno,emailaddress=emailaddress,dob=dob,qualification=qualification,experience=experience,keyskills=keyskills,applieddate=applieddate)
                app.save()
                return render(request,"jsapply.html",{"msg":"Application is Submitted" , 'app':'app'})
            return render(request,"jsapply.html",{'job':job})
    except KeyError:
        return redirect("jobapp:login")
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def appliedjobs(request):
    try:
        if request.session["username"]!=None:
            username=request.session["username"]
            appl=AppliedJobs.objects.all()
            return render(request,"appliedjobs.html",locals())
    except KeyError:
        return redirect("jobapp:login")
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def response(request):
    try:
        if request.session['username']!=None:
            jobseek=JobSeeker.objects.get(emailaddress=request.session["username"])
            if request.method=="POST":
                name = jobseek.name
                contactno = jobseek.contactno
                emailaddress = jobseek.emailaddress       
                responsetype = request.POST['responsetype']
                subject = request.POST['subject']
                responsetext=request.POST['responsetext']
                posteddate = datetime.datetime.today()
                res=Response(name=name,contactno=contactno,emailaddress=emailaddress,responsetype=responsetype,subject=subject,responsetext=responsetext,posteddate=posteddate)
                res.save()
                msg="Your response has been send successfully"
            return render(request,"response.html",locals())
        return render(request,"response.html")
    except KeyError:
        return redirect("jobapp:login")
