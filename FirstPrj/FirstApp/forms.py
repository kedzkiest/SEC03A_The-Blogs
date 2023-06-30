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
        
    def save(self, author, commit=True):
        blog = super(BlogCreateForm, self).save(commit=False)
        blog.author = author
        
        if commit:
            blog.save()
        return blog
    
class SpecifyAuthorForm(forms.Form):
    specified_author = forms.ModelChoiceField(
        queryset=User.objects.all().exclude(is_superuser=True),
        widget=forms.widgets.Select,
        required=False,
        )