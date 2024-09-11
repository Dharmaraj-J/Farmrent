from django.contrib import admin

from . models import UserDetails,Equipment,Requests_Apply

# Register your models here.


admin.site.register(UserDetails)
admin.site.register(Equipment)
admin.site.register(Requests_Apply)