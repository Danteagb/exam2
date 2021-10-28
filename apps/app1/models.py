from django.db import models
import bcrypt
import re
from datetime import datetime

class UserManager(models.Manager):
    def user_validator(self,data):
        errors={}
        if len(data["first_name"])<5:
            errors["first_name"]="First Name should have at least 5 characters"
        if len(data["last_name"])<5:
            errors["last_name"]="Last Name should have at least 5 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(data['email'])==0:
            errors['email'] = "Write your email"
        elif not EMAIL_REGEX.match(data['email']):          
            errors['email'] = "Invalid email address!"
        elif len(User.objects.filter(email= data["email"]))>0:
            errors["email"]="This email already exist"
        if len(data["password"])<8:
            errors["password"]= "Password should have at least 8 characters" 
        if data["confirm_password"]!= data["confirm_password"]:
            errors["confirm"]="Passwords don't match"
        return errors
    def log_validator(self,data):
        errors ={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(data["password"])==0:
            errors["password"]="Please write your password"
        if len(data["email"]) ==0:
            errors["email"]="Please write your email"  
        elif not EMAIL_REGEX.match(data['email']):          
            errors['email'] = "Invalid email address!"      
        elif len(User.objects.filter(email= data["email"]))==0: 
            errors["email"]="This email is not registered"
        else:
            email= data["email"]
            this_user= User.objects.get(email=email)
            if not bcrypt.checkpw(data["password"].encode(), this_user.password.encode()):
                errors["password"]="La contraseña no coincide con este email"
        return errors

    def job_validator(self,data):
        errors={}
        if len(data["title"])==0:
            errors["title"]= "Please write a title" 
        elif len(data["title"])<4:
            errors["title"]= "Title should have at least 4 characters"
        if len(data["description"])==0:
            errors["description"]= "Please write a description"            
        elif len(data["description"])<10:
            errors["description"]= "Description shoul have at least 10 characters"
        if len(data["location"])==0:
            errors["location"]= "Please write a location"
        return errors


class User(models.Model):
    first_name= models.CharField(max_length=50)
    last_name= models.CharField(max_length=50)
    email= models.CharField(max_length=100, unique=True)
    password= models.CharField(max_length=100, default="anything") #Largo para el encriptado de 60 caracteres
    created_at= models.DateTimeField(auto_now=True)
    updated_at= models.DateTimeField(auto_now_add=True)
    objects=UserManager()

class Job(models.Model):
    title= models.CharField( max_length=50)
    creator= models.ForeignKey(User, related_name="this_job", on_delete = models.CASCADE)
    users= models.ManyToManyField(User,related_name="jobs")
    description= models.TextField()
    location= models.CharField(max_length=255)
    created_at= models.DateTimeField(auto_now=True)
    updated_at= models.DateTimeField(auto_now_add=True)
    objects=UserManager()