from django.shortcuts import render,redirect
from django.views.decorators.cache import cache_control
from jobapp.models import JobSeeker,Enquiry,Login
from employer.models import Jobs
from jsapp.models import Response
from . models import News
from datetime import date, datetime

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def my_view(request):
    js = JobSeeker.objects.get(...)  # or your queryset
    age = calculate_age(js.dateofbirth)
    return render(request, "template.html", {"js": js, "age": age})


def test_template(request):
    return render(request, "viewnews.html")

# Create your views here.
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def adminhome(request):
    if 'username' not in request.session or request.session.get('usertype') != 'administrator':
        return redirect('jobapp:login')
    return render(request, 'adminapp/adminhome.html')

def logout(request):
    try:
        del request.session["adminid"]
    except KeyError:
        return redirect("jobapp:login")
    return redirect("jobapp:login")
def news(request):
    if request.method=="POST": 
        newstext=request.POST["newstext"]
        newsdate=datetime.datetime.today()
        new=News(newstext=newstext,newsdate=newsdate)
        new.save()
        return render(request,"news.html",{"msg":"News is added"})
    return render(request,"news.html")
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def viewnews(request):
    try:
        if request.session["adminid"]!=None:
            adminid=request.session["adminid"]
            new=News.objects.all()
            return render(request,"viewnews.html",locals())
    except KeyError:
        return redirect("jobapp:login")
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def viewjobs(request):
    try:
        if request.session["adminid"]!=None:
            adminid=request.session["adminid"]
            new=News.objects.all()
            return render(request,"viewjobs.html",locals())
    except KeyError:
        return redirect("jobapp:login")
def delnews(request,newsdate):
    News.objects.get(newsdate=newsdate).delete() 
    return redirect("adminapp:viewnews")
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def viewenquiries(request):
    try:
        if request.session["adminid"]!=None:
            adminid=request.session["adminid"]
            enq=Enquiry.objects.all()
            return render(request,"viewenquiries.html",locals())
    except KeyError:
        return redirect("jobapp:login")
def delenq(request,emailaddress):
    Enquiry.objects.get(emailaddress=emailaddress).delete()
    return redirect("adminapp:viewenquiries")
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def viewcomplaints(request):
    try:
        if request.session["adminid"]!=None:
            adminid=request.session["adminid"]
            comp=Response.objects.filter(responsetype="complaint")
            return render(request,"viewcomplaints.html",locals())
    except KeyError:
        return redirect("jobapp:login")
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def viewfeedback(request):
    try:
        if request.session["adminid"]!=None:
            adminid=request.session["adminid"]
            feed=Response.objects.filter(responsetype="feedback")
            return render(request,"viewfeedback.html",locals())
    except KeyError:
        return redirect("jobapp:login")
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def viewemployers(request):
    try:
        if request.session["adminid"]!=None:
            adminid=request.session["adminid"]
            emp=Jobs.objects.all()
            return render(request,"viewemployers.html",locals())
    except KeyError:
        return redirect("jobapp:login")
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def viewjobseekers(request):
    try:
        if request.session["adminid"]!=None:
            adminid=request.session["adminid"]
            jobseek=JobSeeker.objects.all()
            return render(request,"viewjobseekers.html",locals())
    except KeyError:
        return redirect("jobapp:login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def terms_page(request):
    try:
        # Optional: only allow logged-in admin to view
        if request.session.get("adminid") is not None:
            adminid = request.session["adminid"]
            return render(request, "terms.html", locals())
    except KeyError:
        # Redirect to login if not logged in
        return redirect("jobapp:login")