from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.conf import settings

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    country = models.CharField(max_length=100)
    birth_date = models.DateField(blank=True, null=True)
    status = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name', 'country', 'birth_date']
    objects = CustomUserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email

class Post(models.Model):
    title = models.CharField(max_length=100)
    blog = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="posts", on_delete=models.CASCADE)

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='ucomments', on_delete= models.CASCADE)
    commentblog = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    comment = models.TextField(blank=True, null=True)
    comment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.comment[:75] if len(self.comment) > 75 else self.comment    

