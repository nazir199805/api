from django.db import models
from django.core.validators import MinValueValidator
from taggit.managers import TaggableManager
from django.contrib.auth.models import User


# =========================================================
# SECTION
# =========================================================

class Section(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to="sections",
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True)
    filter_by = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.name


# =========================================================
# BRAND
# =========================================================

class Brand(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True
    )
    logo = models.ImageField(
        upload_to="brands",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


# =========================================================
# CATEGORY
# =========================================================

class Category(models.Model):

    CATEGORY = (
        ("Oushak", "Oushak"),
        ("Khotan", "Khotan"),
        ("Chobi", "Chobi"),
        ("Kilim", "Kilim"),
        ("Morrocan", "Morrocan"),
    )

    name = models.CharField(
        max_length=300,
        choices=CATEGORY
    )

    def __str__(self):
        return self.name


# =========================================================
# PRODUCT
# =========================================================

class Product(models.Model):

    name = models.CharField(max_length=300)

    # Keep this for compatibility with your existing products.
    # For products with sizes, the actual price will come
    # from ProductSize.
 
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True
    )

    tags = TaggableManager(blank=True)

    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


# =========================================================
# PRODUCT SIZE
# =========================================================

class ProductSize(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="sizes"
    )

    length_cm = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    width_cm = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    length_ft = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    width_ft = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["length_cm", "width_cm"]

    def __str__(self):
        return (
            f"{self.product.name} - "
            f"{self.length_cm} x {self.width_cm} cm / "
            f"{self.length_ft} x {self.width_ft} ft - "
            f"${self.price}"
        )
# =========================================================
# CART
# =========================================================

class Cart(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="cart"
    )

    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"Cart for {self.user.username}"


# =========================================================
# CART ITEM
# =========================================================

class CartItem(models.Model):

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    # NEW: selected rug size
    size = models.ForeignKey(
        ProductSize,
        on_delete=models.PROTECT,
        related_name="cart_items",
        null=True,
        blank=True
    )

    quantity = models.PositiveIntegerField(
        default=1,
        validators=[
            MinValueValidator(1)
        ]
    )

    added_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        if self.size:
            return (
                f"{self.product.name} "
                f"({self.size.width} × "
                f"{self.size.length} {self.size.unit}) "
                f"in {self.cart.user.username}'s cart"
            )

        return (
            f"{self.product.name} "
            f"in {self.cart.user.username}'s cart"
        )

    def total_price(self):

        if self.size:
            return self.size.price * self.quantity

        return self.product.price * self.quantity


# =========================================================
# FAVORITE
# =========================================================

class Favorite(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorites"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("user", "product")

    def __str__(self):
        return (
            f"{self.product.name} "
            f"marked as favorite by "
            f"{self.user.username}"
        )


# =========================================================
# PROFILE
# =========================================================

class Profile(models.Model):

    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default="male"
    )

    def __str__(self):
        return self.gender


# =========================================================
# API
# =========================================================

class Api(models.Model):

    header_sections = models.JSONField(
        default=list
    )

    hero_image = models.ImageField(
        upload_to="images",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Api"
        verbose_name_plural = "Api"

    def __str__(self):
        return "Hero Api"


# =========================================================
# HERO IMAGE
# =========================================================

class HeroImage(models.Model):

    image = models.ImageField(
        upload_to="hero"
    )

    title = models.CharField(
        max_length=255,
        blank=True
    )

    order = models.PositiveIntegerField(
        default=0
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.title or f"Hero Image {self.id}"


# =========================================================
# HERO BUTTON
# =========================================================

class HeroButton(models.Model):

    hero_image = models.ForeignKey(
        HeroImage,
        related_name="buttons",
        on_delete=models.CASCADE
    )

    text = models.CharField(
        max_length=100
    )

    link = models.URLField(
        null=True
    )

    def __str__(self):
        return f"Button: {self.text}"


# =========================================================
# PRODUCT IMAGE
# =========================================================

class ProductImage(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="sub_images"
    )

    image = models.ImageField(
        upload_to="products"
    )

    def __str__(self):
        return f"Image for {self.product.name}"


# =========================================================
# ORDER
# =========================================================

class Order(models.Model):

    STATUS_CHOICES = (
        ("unpaid", "Unpaid"),
        ("paid", "Paid"),
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="unpaid"
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )

    paypal_order_id = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    paypal_capture_id = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    def __str__(self):
        return (
            f"Order #{self.id} "
            f"by {self.user.username}"
        )


# =========================================================
# ORDER ITEM
# =========================================================

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # NEW: preserve the size purchased
    size = models.ForeignKey(
        ProductSize,
        on_delete=models.SET_NULL,
        related_name="order_items",
        null=True,
        blank=True
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    # Store the price at the time of purchase.
    # This is important because product prices can
    # change later.
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):

        product_name = (
            self.product.name
            if self.product
            else "Deleted Product"
        )

        if self.size:
            size_text = (
                f"{self.size.width} × "
                f"{self.size.length} "
                f"{self.size.unit}"
            )

            return (
                f"{self.quantity} x "
                f"{product_name} "
                f"({size_text})"
            )

        return (
            f"{self.quantity} x "
            f"{product_name}"
        )

    def get_total_price(self):
        return self.price * self.quantity