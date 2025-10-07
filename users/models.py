from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User





category = (
    ("women", "Women"),
    ("Men", "Men"),
    ("kids", "Kids")
)


class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)

    def __str__(self):
        return self.name


class category(models.Model):
    name = models.CharField(max_length=300, choices=category)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    color = models.CharField(max_length=300, null=True, blank=True)
    category = models.ForeignKey(category, on_delete=models.SET_NULL, null=True)
    tags = TaggableManager(blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return self.name



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')  # Linking to user
    is_active = models.BooleanField(default=False)  # To track if the cart is active

    def __str__(self):
        return f"Cart for {self.user.username}"



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])  
    added_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.product.name} in {self.cart.user.username}'s cart"
    
    def total_price(self):
        return self.product.price * self.quantity




class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  
    created_at = models.DateTimeField(auto_now_add=True)  

    class Meta:
        unique_together = ('user', 'product')  

    def __str__(self):
        return f"{self.product.name} marked as favorite by {self.user.username}"



class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()  
    created_at = models.DateTimeField(auto_now_add=True)  
    is_read = models.BooleanField(default=False)  # To track if the user has read the notification
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Notification for {self.user.username} - {'Read' if self.is_read else 'Unread'}"

    def mark_as_read(self):
        self.is_read = True
        self.save()






class Profile(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male')


    def __str__(self):
        return self.gender





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





class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sub_images')
    image = models.ImageField(upload_to='products')
    

    def __str__(self):
        return f"Image for {self.product.name}"
    


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"
    



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)


    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.id}"

    def get_total_price(self):
        return self.price * self.quantity

