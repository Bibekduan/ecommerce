from django.contrib import admin
from .models import User,Profile,ContactUs
class useradmin(admin.ModelAdmin):
    list_display=['username','email','bio']

# class ProfileAdmin(admin.ModelAdmin):
#     list_display=['full_name','bio','phone','verified']
class ContactUsAdmin(admin.ModelAdmin):
    list_display=['full_name','email','subject']
# Register your models here.
admin.site.register(User,useradmin)
admin.site.register(Profile)
admin.site.register(ContactUs,ContactUsAdmin)
