from django.contrib import admin
from .models import Api, offer, HeroImage, HeroButton, Catagory, Profile, Product, ProductImage
from unfold.admin import ModelAdmin
from image_uploader_widget.admin import ImageUploaderInline
from image_uploader_widget.widgets import ImageUploaderWidget
from django.db import models


class HeroImageAdmin(ModelAdmin):
    formfield_overrides = {
        models.ImageField: {'widget': ImageUploaderWidget},
    }

class ProductImagesTab(ImageUploaderInline):
    model = ProductImage

class ProductAdmin(ModelAdmin):
    list_display = ['name', 'price']
    inlines = [ProductImagesTab]

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