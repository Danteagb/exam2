from django.shortcuts import render,HttpResponse,redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return redirect("/login")

def create_user(request):
    if request.method=="GET":
        return render(request,"registration.html")
    elif request.method=="POST":
        errors= User.objects.user_validator(request.POST)
        if len(errors)>0:
            nombre= request.POST["first_name"]
            apellido= request.POST["last_name"]
            mail=request.POST["email"]
            context={
                "first_name":nombre,
                "last_name":apellido,
                "email":mail,
            }
            for key,value in errors.items():
                messages.error(request,value,key)
            return render(request,"registration.html",context)
        this_user=User(
            first_name= request.POST["first_name"],
            last_name= request.POST["last_name"],
            email=request.POST["email"],
            password=request.POST["password"],
        )
        passwordhash= bcrypt.hashpw(this_user.password.encode(), bcrypt.gensalt())
        this_user.password = passwordhash.decode()
        this_user.save()
        request.session["user_id"]= this_user.id
        # request.session["user_id"]=this_user.id
        return redirect("/dashboard")

def login(request):
    if request.method=="GET":
        return render(request,"login.html")
    elif request.method=="POST":
        errors= User.objects.log_validator(request.POST)
        this_email = request.POST["email"]
        if len(errors)>0:
            email= request.POST["email"]
            context={
                "email":email,
            }
            for key,value in errors.items():
                messages.error(request,value,key)
            return render(request,"login.html",context)
        usuario= User.objects.filter(email=this_email) #Filter arroja una lista
        if usuario: #Lista vacía arroja False
            logged_user = usuario[0]
            request.session["user_id"]= logged_user.id
            return redirect("/dashboard")       
        return redirect("/dashboard")
    
def logout(request):
    del request.session["user_id"]
    return redirect("/login") 

def dashboard(request):
    if "user_id" in request.session:
        this_id= request.session["user_id"]
        this_user= User.objects.get(id=this_id)
        this_user_email= this_user.email
        his_jobs= Job.objects.filter(creator__email=this_user_email).exclude(users__email=this_user_email)
        other_jobs= Job.objects.exclude(creator__email=this_user_email).exclude(users__email=this_user_email)
        join_jobs= Job.objects.filter(users__email=this_user_email)
        context={
            "this_user":this_user,
            "creator_jobs":his_jobs,
            "other_jobs":other_jobs,
            "join_jobs": join_jobs,
        }
        return render(request,"dashboard.html",context)
    else:
        return render(request,"fail_succes.html")


def add_job(request):
    if "user_id" in request.session:
        this_id=request.session["user_id"]
        this_user= User.objects.get(id=this_id)
        if request.method=="GET":
            context={
                "this_user": this_user
            }
            return render(request,"add_job.html",context)
        elif request.method=="POST":
            errors= User.objects.job_validator(request.POST)
            if len(errors)>0:
                titulo= request.POST["title"]
                descripcion= request.POST["description"]
                locacion= request.POST["location"]
                context={
                    "title":titulo,
                    "description": descripcion,
                    "location": locacion,
                }
                for key,value in errors.items():
                    messages.error(request,value,key)
                return render(request,"add_job.html",context)
            this_job=Job(
                title= request.POST["title"],
                description=request.POST["description"],
                location= request.POST["location"],
                creator=this_user
            )            
            this_job.save()
            #this_job.user.add(this_user)
            return redirect("/dashboard")
        return redirect("/dashboard")
    else:
        return render(request,"fail_succes")

def show_job(request,job_id):
    if "user_id" in request.session:
        context={
            "this_job": Job.objects.get(id=job_id),
        }
        return render(request,"views.html", context)
    else:
        return render(request,"fail_succes.html")

def edit_job(request,job_id):
    this_job= Job.objects.get(id=job_id)
    if "user_id" in request.session:
        if request.method=="GET":
            context={
                    "this_job": this_job,
                }
            return render(request,"edit.html", context)
        elif request.method=="POST":
            errors= User.objects.job_validator(request.POST)
            if len(errors)>0:
                context={
                    "this_job":this_job,
                }
                for key,value in errors.items():
                    messages.error(request,value,key)
                return render(request,"edit.html",context)
            this_job.title=request.POST["title"]
            this_job.description=request.POST["description"]
            this_job.location=request.POST["location"]
            this_job.save()
            return redirect("/dashboard")
    else:
        return render(request,"fail_succes")


def join(request,job_id):
    if "user_id" in request.session:
        this_job = Job.objects.get(id=job_id)
        user_id= request.session["user_id"]
        this_user=User.objects.get(id=user_id)
        this_job.users.add(this_user)
        return redirect("/dashboard")
    else:
        return render(request,"fail_succes.html")

def delete(request,job_id):
    if "user_id" in request.session:
        this_job= Job.objects.get(id=job_id)
        this_job.delete()
        return redirect("/dashboard")
    else:
        return render(request,"fail_succes.html")