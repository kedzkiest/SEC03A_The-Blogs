from . import views
from django.urls import path

urlpatterns = [
    path("home", views.home_view, name="home"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("user/", views.user_view, name="user"),
    path("other/", views.other_view, name="other"),
    path("blog/<int:pk>/", views.blog_detail_view, name="blog_detail")
]