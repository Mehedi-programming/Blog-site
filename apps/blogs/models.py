from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils import timezone


User = get_user_model()


# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)


    def __str__(self):
        return self.name
    
    
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reading_time = models.PositiveSmallIntegerField(default=1)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    
class PostVersion(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='versions')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-created_at']
        
        
class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='bookmarked_by')
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ('user', 'post')
        
        
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)


    class Meta:
        ordering = ['created_at']