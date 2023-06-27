from django.db import models
from django.contrib.auth.models import User

# Create your models here.
'''
class Author(AbstractUser):
    username = None
    email = models.EmailField("email address", unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
'''

class Blog(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=50, default=None)
    content = models.TextField(default=None)
    date = models.DateField(auto_now_add=True)
    is_public = models.BooleanField(default=False)
  
    def __str__(self):
        return self.title
    
    