from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Blog

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email"]
        
class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["username", "password"]
        
class BlogCreateForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ["author", "title", "content", "is_public"]
        
    def save(self, author, commit=False):
        blog = super(BlogCreateForm, self).save(commit=False)
        
        # author information is provided automatically (not in the form)
        Blog.objects.create(
            author=author,
            title=blog.title,
            content=blog.content,
            is_public=blog.is_public,
        )
        
        