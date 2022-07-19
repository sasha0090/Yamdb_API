from django.db import models
from django.core.validators import validate_slug


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        unique=True,
        max_length=50,
        validators=[validate_slug])

    class Meta:
        verbose_name = 'Категория'
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Жанр'
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.DateField(null=True, blank=True)
    description = models.TextField()
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL, related_name='genre')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='category')
#    review = models.ForeignKey(
#        Review, on_delete=models.CASCADE, related_name='review')
