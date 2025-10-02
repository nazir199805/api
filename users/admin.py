from django.contrib import admin
from .models import Api, offer, HeroImage, HeroButton, Product, ProductImage, Catagory

class ProductImagesTab(admin.TabularInline):
    model = ProductImage

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    inlines = [ProductImagesTab]



admin.site.register(Api)
admin.site.register(offer)
admin.site.register(HeroImage)
admin.site.register(HeroButton)
admin.site.register(Catagory)
admin.site.register(Product, ProductAdmin)