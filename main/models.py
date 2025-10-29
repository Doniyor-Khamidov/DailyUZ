from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="category/", null=True, blank=True)
    slug = models.SlugField(max_length=256, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=256, unique=True, blank=True, null=True)
    intro = models.TextField()
    image = models.ImageField(upload_to="article/", null=True, blank=True)
    reading_time = models.DurationField(blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    published = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    important = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.important:
            Article.objects.exclude(pk=self.pk).update(important=False)

        base_slug = slugify(self.title)
        unique_slug = base_slug
        count = 0

        while Article.objects.exclude(pk=self.pk).filter(slug=unique_slug).exists():
            unique_slug = base_slug + str(count)
            count += 1

        self.slug = unique_slug

        super().save(*args, **kwargs)


class Context(models.Model):
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="context/", null=True, blank=True)

    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return self.article.title


class Comment(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    text = models.TextField()
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Moment(models.Model):
    title = models.CharField(max_length=255)
    picture = models.ImageField(upload_to="moment/")
    author = models.CharField(max_length=255, blank=True, null=True)
    published = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=14, blank=True, null=True)
    subject = models.CharField(max_length=255)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Newsletter(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email
