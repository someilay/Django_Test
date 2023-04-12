from django.contrib import admin
from . import models


@admin.register(models.Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(models.Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent', 'menu']
