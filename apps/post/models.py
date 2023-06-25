from django.db import models
from django.contrib.auth import get_user_model
from slugify import slugify
from .utils import get_time



User = get_user_model()


class Post(models.Model):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('draft', 'Draft')
    )

    user = models.ForeignKey(
        verbose_name='Автор поста',
        to=User,
        on_delete=models.CASCADE,
        related_name='publications'
    )
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, primary_key=True, blank=True)
    text = models.TextField()
    image = models.ImageField(upload_to='post_images')
    status = models.CharField(
        max_length=12, 
        choices=STATUS_CHOICES, 
        default='draft')
    tag = models.ManyToManyField(
        to='Tag',
        related_name='publications',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title + get_time())
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('created_at', )


class PostImage(models.Model):
    image = models.ImageField(upload_to='post_images/carousel')
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name='post_images'
    )


class Tag(models.Model):
    title = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(primary_key=True, blank=True, max_length=35)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Comment(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment from {self.user.username} to {self.post.title}'


class Rating(models.Model):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    RATING_CHOICES = (
        (ONE, '1'),
        (TWO, '2'),
        (THREE, '3'),
        (FOUR, '4'),
        (FIVE, '5')
    )

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES, 
        blank=True, 
        null=True)
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name='ratings'
    )

    def __str__(self):
        return str(self.rating)


class Like(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name='likes'
    )

    def __str__(self) -> str:
        return f'Liked by {self.user.username}'