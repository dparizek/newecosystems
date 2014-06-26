from django.contrib import admin
from .models import *


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'lab_group')
    search_fields = ('user', 'lab_group')
