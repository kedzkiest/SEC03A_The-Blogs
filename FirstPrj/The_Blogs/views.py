from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignupForm, LoginForm, BlogCreateForm, ConditionForm
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Blog
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import FirstPrj.UserDefinedConstValue as UserDefinedConstValue

MAX_POST_PER_PAGE = 5

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

def redirect_to_home_view(request):
    return redirect(to="/" + UserDefinedConstValue.APPNAME + "/home")
    
# Create your views here.
def home_view(request):
    user = request.user
    
    if request.method == "POST":
        blog_condition_form = ConditionForm(request.POST)
        request.session["form_data"] = request.POST
    else:
        blog_condition_form = ConditionForm(request.session.get("form_data"))

    blogs = Blog.objects.exclude(is_public=False).order_by("-created_at")
    
    if "form_data" in request.session:
        # The author to focus
        specified_author = request.session["form_data"].get("specified_author")
        if specified_author:
            blogs = blogs.filter(author=specified_author)
        
        # The date to focus
        specified_date = request.session["form_data"].get("specified_date")
        if specified_date:
            blogs = blogs.filter(created_at__date=specified_date)
    
    paginated_blogs = paginate_queryset(request, blogs, MAX_POST_PER_PAGE)
    
    params = {
        "user_login": user.is_authenticated,
        "blog_condition_form": blog_condition_form,
        "blogs": paginated_blogs.object_list,
        "page_obj": paginated_blogs,
    }
    
    return render(request, UserDefinedConstValue.APPNAME + "/home.html", params)

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        
        if form.is_valid(): 
            form.save()
            return redirect(to="/" + UserDefinedConstValue.APPNAME + "/login/")
        
    else:
        form = SignupForm()
    
    param = {
        "form": form
    }
    
    return render(request, UserDefinedConstValue.APPNAME + "/signup.html", param)

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        next = request.POST.get("next")
        
        if form.is_valid(): 
            user = form.get_user()
            
            if user:
                login(request, user)
        
        if next == "None":
            return redirect(to="/" + UserDefinedConstValue.APPNAME + "/user/")
        else:
            return redirect(to=next)
        
    else:
        form = LoginForm()
        next = request.GET.get("next")
    
    param = {
        "form": form,
        "next": next,
    }
    
    return render(request, UserDefinedConstValue.APPNAME + "/login.html", param)

def logout_view(request):
    logout(request)
    
    return render(request, UserDefinedConstValue.APPNAME + "/logout.html")

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
    
    return render(request, UserDefinedConstValue.APPNAME + "/user.html", params)

def other_view(request):
    users = User.objects.exclude(is_superuser=True)
    
    params = {
        "users": users
    }
    
    return render(request, UserDefinedConstValue.APPNAME + "/other.html", params)

def blog_detail_view(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    
    params = {
        "blog": blog
    }
    return render(request, UserDefinedConstValue.APPNAME + "/blog_detail.html", params)

@login_required
def blog_add_view(request):
    if request.method == "POST":
        form = BlogCreateForm(request.POST)

        if form.is_valid():
            # Since "author" field is a foreign key in Blog model, it should be provided automatically (not in BlogCreateForm),
            # I give "author" information as an argument when saving the form.
            form.save(author = request.user)
            return redirect("user")
    
    else:
        form=BlogCreateForm()
        
    params = {
        "form": form,
    }
    
    return render(request, UserDefinedConstValue.APPNAME + "/blog_add.html", params)

@login_required
def blog_update_view(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    form = BlogCreateForm(request.POST or None, instance=blog)
    
    if request.method == "POST":

        if form.is_valid():
            # Since "author" field is a foreign key in Blog model, it should be provided automatically (not in BlogCreateForm),
            # I give "author" information as an argument when saving the form.
            form.save(author = request.user)
            return redirect("user")
        
    params = {
        "form": form,
    }
    
    return render(request, UserDefinedConstValue.APPNAME + "/blog_add.html", params)

@login_required
def blog_delete_view(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    
    if request.method == "POST":
        blog.delete()
        return redirect("user")
    
    params = {
        "blog": blog,
    }
    
    return render(request, UserDefinedConstValue.APPNAME + "/blog_delete.html", params)

from turbo.shortcuts import render_frame, render_frame_string
from The_Blogs.streams import AppStream

def signupTest(request):
    r = render_frame(
        request,
        UserDefinedConstValue.APPNAME + "/signup_form_frame.html",
        {"signup_form": SignupForm()},
    ).update(id="main_box")

    AppStream().stream(r)

    return HttpResponse("")

def do_signupTest(request):
    form = SignupForm(request.POST)
    
    signup_result = ""
    
    if form.is_valid(): 
        form.save()
        signup_result = "Signup successful!"
    else:
        signup_result = str(form.errors)


    AppStream().update(text=signup_result, id="main_box")

    return (
        render_frame(request, "register_form_frame.html", {"register_form": signup_result})
        .update(id="signup_form_frame")
        .response
    )