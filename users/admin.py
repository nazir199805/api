from django.contrib import admin
from .models import Api, offer, HeroImage, HeroButton, Product, ProductImage, Catagory, Profile
from unfold.admin import ModelAdmin

class ProductImagesTab(admin.TabularInline):
    model = ProductImage

class ProductAdmin(ModelAdmin):
    list_display = ['name', 'price']
    inlines = [ProductImagesTab]

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user_first_name','user_email', 'gender']

    def user_first_name(self, obj):
        return obj.user.first_name
    user_first_name.short_description = 'First Name'

    def user_email(self, obj):
        return obj.user.email


admin.site.register(Api)
admin.site.register(offer)
admin.site.register(HeroImage)
admin.site.register(HeroButton)
admin.site.register(Catagory)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Product, ProductAdmin)