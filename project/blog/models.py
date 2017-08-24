from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    title = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.title


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    category = models.ManyToManyField(Category)
    title = models.CharField(max_length=200, blank=False)
    text = RichTextUploadingField()
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-published_date']

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
