from django.contrib import admin
from .models import Api, offer, HeroImage, HeroButton, Category, Profile, Product, ProductImage
from unfold.admin import ModelAdmin
from image_uploader_widget.admin import ImageUploaderInline
from image_uploader_widget.widgets import ImageUploaderWidget
from django.db import models
from .models import Product, Favorite, Cart, CartItem, Notification,Order, OrderItem, Brand
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm, SelectableFieldsExportForm


admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    # Forms loaded from `unfold.forms`
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass





class ProductImagesTab(ImageUploaderInline):
    model = ProductImage


class ProductAdmin(ModelAdmin):
    list_display = ('name', 'price', 'category',) 
    search_fields = ('name', 'category__name')  # Fields to search
    list_filter = ('category',)  # Add filters in the admin panel
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


class NotificationAdmin(ModelAdmin):
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

class OrderAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ['user', 'status', 'total_amount']
    import_form_class = ImportForm
    export_form_class = ExportForm

class OrderItemAdmin(ModelAdmin):
    pass

class BrandAdmin(ModelAdmin):
    pass


admin.site.register(Api)
admin.site.register(Brand, BrandAdmin)
admin.site.register(offer, OfferAdmin)
admin.site.register(HeroImage, HeroImageAdmin)
# admin.site.register(HeroButton)
admin.site.register(Category, CaatagoryAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(HeroButton, ButtonAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
