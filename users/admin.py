from django.contrib import admin
from .models import Api, offer, HeroImage, HeroButton, Catagory, Profile, Product, ProductImage
from unfold.admin import ModelAdmin
from image_uploader_widget.admin import ImageUploaderInline
from image_uploader_widget.widgets import ImageUploaderWidget
from django.db import models
from .models import Product, Favorite, Cart, CartItem, Notification


class ProductImagesTab(ImageUploaderInline):
    model = ProductImage


class ProductAdmin(ModelAdmin):
    list_display = ('name', 'price', 'catagory', 'is_favorite') 
    search_fields = ('name', 'catagory__name')  # Fields to search
    list_filter = ('catagory', 'is_favorite')  # Add filters in the admin panel
    inlines = [ProductImagesTab]





class FavoriteAdmin(ModelAdmin):
    list_display = ('user', 'product', 'created_at') 
    search_fields = ('user__username', 'product__name') 


admin.site.register(Favorite, FavoriteAdmin)


class CartAdmin(ModelAdmin):
    list_display = ('user', 'is_active')   
    search_fields = ('user__username',) 
    list_filter = ('is_active',)  


admin.site.register(Cart, CartAdmin)


class CartItemAdmin(ModelAdmin):
    list_display = ('cart', 'product', 'quantity')  
    search_fields = ('cart__user__username', 'product__name')  
    list_filter = ('cart__is_active',) 


admin.site.register(CartItem, CartItemAdmin)


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    list_filter = ('is_read',)
    search_fields = ('message',)

admin.site.register(Notification, NotificationAdmin)



class HeroImageAdmin(ModelAdmin):
    formfield_overrides = {
        models.ImageField: {'widget': ImageUploaderWidget},
    }




class ProfileAdmin(ModelAdmin):
    list_display = ['user_first_name','user_email', 'gender']

    def user_first_name(self, obj):
        return obj.user.first_name
    user_first_name.short_description = 'First Name'

    def user_email(self, obj):
        return obj.user.email

class CaatagoryAdmin(ModelAdmin):
    pass


class ButtonAdmin(ModelAdmin):
    pass

class OfferAdmin(ModelAdmin):
    pass


admin.site.register(Api)
admin.site.register(offer, OfferAdmin)
admin.site.register(HeroImage, HeroImageAdmin)
# admin.site.register(HeroButton)
admin.site.register(Catagory, CaatagoryAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(HeroButton, ButtonAdmin)