from django.db import models
from PIL import Image


class Timestamp(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def get_image_path(instance, filename):
    return '/'.join([instance.slug, filename])


class Book(Timestamp):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField(max_length=255)
    image = models.ImageField(upload_to=get_image_path, blank=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        super(Book, self).save(*args, **kwargs)
        if self.image:
            image = Image.open(self.image)
            i_width, i_height = image.size
            max_size = (800, 800)

            if i_width > 800:
                image.thumbnail(max_size, Image.ANTIALIAS)
                image.save(self.image.path)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name
