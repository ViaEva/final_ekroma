from django.contrib import admin
from .models import Post, Tag, Rating, PostImage, Like, Comment

admin.site.register([Post, Tag, Rating, PostImage, Like, Comment])
