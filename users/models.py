from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from taggit.managers import TaggableManager





class Api(models.Model):
    header_sections = models.JSONField(default=list)
    hero_image = models.ImageField(upload_to='images', null=True,blank=True)

    
    class Meta:
        verbose_name = "Api"
        verbose_name_plural = "Api"

    def __str__(self):
      return f'Hero Api'
    

  
class offer(models.Model):
   timer = models.IntegerField()
   offer = models.IntegerField(null=True, blank=True)



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


CATAGORY = (
    ("women", "Women"),
    ("Men", "Men"),
    ("kids", "Kids")
)


class Catagory(models.Model):
    name = models.CharField(max_length=300, choices=CATAGORY)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=300)
    main_image = models.ImageField(upload_to='products')
    price = models.DecimalField(max_digits=10,decimal_places=2)
    color = models.CharField(max_length=300, null=True, blank=True)
    catagory = models.ForeignKey(Catagory, on_delete=models.SET_NULL, null=True)
    is_favorite = models.BooleanField(default=False, null=True, blank=True) 
    tags = TaggableManager()

    def __str__(self):
        return self.name





class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sub_images')
    image = models.ImageField(upload_to='products')
    

    def __str__(self):
        return f"Image for {self.product.name}"