from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    title = models.CharField(max_length=50, blank=False)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Post(models.Model):
    author = models.ForeignKey('accounts.Account')
    category = models.ManyToManyField(Category, related_name='posts')
    title = models.CharField(max_length=200, blank=False)
    text = RichTextUploadingField()
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(null=True, blank=True)
    is_draft = models.BooleanField(default=True)

    class Meta:
        ordering = ['-published_date']

    def publish(self):
        self.published_date = timezone.now()
        self.is_draft = True
        self.save()

    def __str__(self):
        return self.title
