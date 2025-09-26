from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class User(models.Model):
    header_sections = models.JSONField(default=list)
    hero_image = models.ImageField(upload_to='images', null=True,blank=True)

    def __str__(self):
      return f'{self.id}'
  