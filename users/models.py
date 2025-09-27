from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class User(models.Model):
    header_sections = models.JSONField(default=list)
    hero_image = models.ImageField(upload_to='images', null=True,blank=True)

    
    class Meta:
        verbose_name = "Api"
        verbose_name_plural = "Api"

    def __str__(self):
      return f'Hero Api'
    

  
class offer(models.Model):
   timer = models.IntegerField()
   offer = models.IntegerField(null=True)



class HeroImage(models.Model):
    image = models.ImageField(upload_to='hero/')
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title or f"Hero Image {self.id}"
    

class HeroButton(models.Model):
    hero_image = models.ForeignKey(HeroImage, related_name='buttons', on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    link = models.URLField(null=True)

    def __str__(self):
        return f"Button: {self.text}"
