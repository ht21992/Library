from django.db import models
from django.urls import reverse
from uuid import uuid4
from django.core.validators import (
    FileExtensionValidator,
    MaxValueValidator,
    MinValueValidator,
)
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify

from io import BytesIO
from PIL import Image
from django.core.files import File


from botocore.exceptions import ParamValidationError
import os
from django.contrib.auth.models import User


class Genere(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Generes"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Character(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Characters"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=500, blank=False, verbose_name="title")
    author = models.CharField(max_length=500, blank=False, verbose_name="author")
    publisher = models.CharField(max_length=500, blank=True, verbose_name="publisher")
    series = models.CharField(max_length=500, blank=True, verbose_name="series")
    language = models.CharField(max_length=500, blank=True, verbose_name="language")

    isbn = models.CharField(max_length=500, blank=True, verbose_name="isbn")
    description = models.TextField(verbose_name="description", blank=False)

    geners = models.ManyToManyField(
        Genere,
        blank=True,
        verbose_name="generes",
    )

    characters = models.ManyToManyField(
        Character,
        blank=True,
        verbose_name="characters",
    )
    rating = models.FloatField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
    )
    pages = models.IntegerField(default=0, blank=True)
    price = models.DecimalField(blank=True, max_digits=19, decimal_places=2, null=True)
    image = models.URLField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        verbose_name = "book"
        verbose_name_plural = "books"
        ordering = ('-updated',)

    def __str__(self) -> str:
        return f"{self.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
