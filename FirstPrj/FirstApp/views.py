from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignupForm, LoginForm, BlogCreateForm
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Blog
from django.contrib.auth.decorators import login_required

# Create your views here.
def home_view(request):
    blogs = Blog.objects.exclude(is_public=False)
    
    params = {
        "blogs": blogs,
    }
    
    return render(request, "FirstApp/home.html", params)

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        
        if not form.is_valid(): 
            return HttpResponse("Invalid form") 
        
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
        
        if not form.is_valid(): 
            return HttpResponse("Invalid form")
        
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
    if not user.is_authenticated: 
        return HttpResponse("You are not logged in")
    
    user_written_blogs = Blog.objects.filter(author=user)
    
    params = {
        "user": user,
        "blogs": user_written_blogs,
    }
    
    return render(request, "FirstApp/user.html", params)

@login_required
def other_view(request):
    users = User.objects.exclude(username=request.user.username)
    
    params = {
        "users": users
    }
    
    return render(request, "FirstApp/other.html", params)

def blog_detail_view(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    
    params = {
        "blog": blog
    }
    return render(request, "FirstApp/blog_detail.html", params)

@login_required
def blog_add_view(request):
    if request.method == "POST":
        form = BlogCreateForm(request.POST)
        
        if not form.is_valid():
            print(form.errors)
            return HttpResponse("Invalid form")
        
        # Since "author" field is provided automatically (not in BlogCreateForm),
        # I give "author" information as an argument when saving the form.
        form.save(request.user)
        return redirect("user")
    
    else:
        form=BlogCreateForm()
        
    params = {
        "form": form,
    }
    
    return render(request, "FirstApp/blog_add.html", params)

@login_required
def blog_delete_view(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    
    if request.method == "POST":
        blog.delete()
        return redirect("user")
    
    params = {
        "blog": blog,
    }
    
    return render(request, "FirstApp/blog_delete.html", params)