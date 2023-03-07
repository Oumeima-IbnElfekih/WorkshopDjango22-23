from django.shortcuts import render,redirect
from .forms import *
from django.contrib.auth import login,authenticate
from .models import *

# Create your views here.

def login_def(req):
    form =LoginForm()
    if req.method=="POST":
        username =req.POST['username']
        pwd=req.POST['password']
        user= authenticate(req,username=username,password=pwd)
        if user is not None:
            login(req,user)
            return redirect('event_list_view')
        else:
            return redirect('login')
    return render(req,"users/form.html",{"form":form})        

def register(req):
    form = RegisterForm()
    if req.method=="POST":
        print(req.POST)
        form =RegisterForm(req.POST)
        if form.is_valid():
            user=form.save()
            login(req,user=user)
            return redirect('event_list_view')
       
    return render(req,"users/form.html",{"form":form})