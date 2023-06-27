from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Blog
from django.contrib.auth.decorators import login_required

# Create your views here.
def home_view(request):
    blogs = Blog.objects.all()
    
    params = {
        "blogs": blogs,
    }
    
    return render(request, "FirstApp/home.html", params)

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        
        if not form.is_valid(): return HttpResponse("Invalid form") 
        
        form.save()
        
    else:
        form = SignupForm()
    
    param = {
        "form": form
    }
    
    return render(request, "FirstApp/signup.html", param)

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        next = request.POST.get("next")
        
        if not form.is_valid(): return HttpResponse("Invalid form")
        user = form.get_user()
        
        if not user: return HttpResponse("Invalid user")
        login(request, user)
        
        if next == "None":
            return redirect(to="/FirstApp/user/")
        else:
            return redirect(to=next)
        
    else:
        form = LoginForm()
        next = request.GET.get("next")
    
    param = {
        "form": form,
        "next": next,
    }
    
    return render(request, "FirstApp/login.html", param)

def logout_view(request):
    logout(request)
    
    return render(request, "FirstApp/logout.html")

@login_required
def user_view(request):
    user = request.user
    if not user.is_authenticated: return HttpResponse("You are not logged in")
    
    params = {
        "user": user
    }
    
    return render(request, "FirstApp/user.html", params)

@login_required
def other_view(request):
    users = User.objects.exclude(username=request.user.username)
    
    params = {
        "users": users
    }
    
    return render(request, "FirstApp/other.html", params)