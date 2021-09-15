from django.db import models
from django.db.models.fields import related
from django.db.models.fields.reverse_related import OneToOneRel
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.


def user_directory_path(instance, filename):
    return 'post/{0}/{1}'.format(instance.id, filename)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post (models.Model):

    class Newmanager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    excerpt = models.TextField(
        max_length=250, default='Short few words about the post')
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    publish = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts')
    image = models.ImageField(
        upload_to=user_directory_path, default='post/default.jpg')
    content = models.TextField()
    status = models.CharField(max_length=10, choices=options, default='draft')
    objects = models.Manager()
    newmanager = Newmanager()

    def get_absolute_url(self):
        return reverse('blog:post_single', args=[self.slug])

    class Meta:
        ordering = ('publish',)

    def __str__(self):
        return self.title


class Comment(MPTTModel):

    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    parent = TreeForeignKey('self',
                            on_delete=models.CASCADE,
                            null=True,
                            blank=True,
                            related_name='children')
    name = models.CharField(max_length=50)
    email = models.EmailField()
    content = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ['publish']

    def __str__(self):
        return f"Comment by {self.name}"
