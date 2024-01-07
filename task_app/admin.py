from django.contrib import admin
from .models import *


# Register your models here.

class UserRegistrationModelAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'role_type')
    
admin.site.register(RegistrationModel, UserRegistrationModelAdmin)

admin.site.register(MassRoleDetailModel)
# admin.site.register(RegistrationModel)
admin.site.register(CategoryModel)
admin.site.register(ContentModel)


