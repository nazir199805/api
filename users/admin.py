from django.contrib import admin
from .models import User, offer, HeroImage, HeroButton

# Register your models here.

admin.site.register(User)
admin.site.register(offer)
admin.site.register(HeroImage)
admin.site.register(HeroButton)