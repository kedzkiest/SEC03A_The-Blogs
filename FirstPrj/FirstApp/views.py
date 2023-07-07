from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignupForm, LoginForm, BlogCreateForm, ConditionForm
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Blog
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def paginate_queryset(request, queryset, count):
    paginator = Paginator(queryset, count)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    return page_obj
    
# Create your views here.
def home_view(request):
    if request.method == "POST":
        blog_condition_form = ConditionForm(request.POST)
        request.session["form_data"] = request.POST
    else:
        blog_condition_form = ConditionForm(request.session.get("form_data"))

    blogs = Blog.objects.exclude(is_public=False).order_by("-created_at")
    
    # The author to focus
    specified_author = request.session["form_data"].get("specified_author")
    if specified_author:
        blogs = blogs.filter(author=specified_author)
        
    # The date to focus
    specified_date = request.session["form_data"].get("specified_date")
    if specified_date:
        blogs = blogs.filter(created_at__date=specified_date)
    
    post_num_per_page = 5
    paginated_blogs = paginate_queryset(request, blogs, post_num_per_page)
    
    params = {
        "blog_condition_form": blog_condition_form,
        "blogs": paginated_blogs.object_list,
        "page_obj": paginated_blogs,
    }
    
    return render(request, "FirstApp/home.html", params)

def signup_view(request):
    if request.method == "POST":
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
    
    user_written_blogs = Blog.objects.filter(author=user).order_by("-created_at")
    
    params = {
        "user": user,
        "blogs": user_written_blogs,
    }
    
    return render(request, "FirstApp/user.html", params)

def other_view(request):
    users = User.objects.exclude(is_superuser=True)
    
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
        form.save(author = request.user)
        return redirect("user")
    
    else:
        form=BlogCreateForm()
        
    params = {
        "form": form,
    }
    
    return render(request, "FirstApp/blog_add.html", params)

@login_required
def blog_update_view(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    form = BlogCreateForm(request.POST or None, instance=blog)
    
    if request.method == "POST":

        if not form.is_valid():
            print(form.errors)
            return HttpResponse("Invalid form")
        
        # Since "author" field is provided automatically (not in BlogCreateForm),
        # I give "author" information as an argument when saving the form.
        form.save(author = request.user)
        return redirect("user")
        
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