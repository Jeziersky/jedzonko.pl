from django.db import models
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.TextField()
    description = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now_add=timezone.now)
    preparation = models.TextField()
    preparation_time = models.IntegerField()
    votes = models.IntegerField(default=0)


class Plan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    recipe = models.ManyToManyField(Recipe, through="RecipePlan")


class DayName(models.Model):
    name = models.CharField(max_length=16)
    order = models.IntegerField()


class RecipePlan(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.DO_NOTHING)
    plan = models.ForeignKey(Plan, on_delete=models.DO_NOTHING)
    day_name = models.ForeignKey(DayName, on_delete=models.DO_NOTHING)
    meal_name = models.CharField(max_length=255)
    order = models.IntegerField()


class Page(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.CharField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Page, self).save(*args, **kwargs)


