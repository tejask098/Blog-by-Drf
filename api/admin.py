from django.contrib import admin
from api.models import Post, User, Comment


@admin.register(Post)
class Postadmin(admin.ModelAdmin):
    list_display = ["title", "blog", "author"]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "country", "birth_date")


@admin.register(Comment)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "commentblog", "comment", "comment_date")