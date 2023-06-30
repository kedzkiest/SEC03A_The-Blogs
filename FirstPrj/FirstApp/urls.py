from . import views
from django.urls import path

urlpatterns = [
    path("home", views.home_view, name="home"),
    
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    
    path("user/", views.user_view, name="user"),
    path("other/", views.other_view, name="other"),
    
    path("blog/add/", views.blog_add_view, name="blog_add"),
    path("blog/update/<int:pk>/", views.blog_update_view, name="blog_update"),
    path("blog/detail/<int:pk>/", views.blog_detail_view, name="blog_detail"),
    path("blog/delete/<int:pk>/", views.blog_delete_view, name="blog_delete"),
]