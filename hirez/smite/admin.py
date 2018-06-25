from django.contrib import admin

from . import models


class GodAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'role', 'type', 'pantheon')
    list_filter = ('role', 'type', 'pantheon')
    search_fields = ['name']


class ItemStatAdmin(admin.ModelAdmin):
    list_display = ('value', 'stat', 'item')
    list_filter = ('stat', 'item')


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'tier', 'price', 'type', 'starting_item')
    list_filter = ('tier', 'type', 'starting_item')
    search_fields = ['name']


# Register your models here.
admin.site.register(models.God, GodAdmin)
admin.site.register(models.Item, ItemAdmin)
admin.site.register(models.ItemDescription)
admin.site.register(models.ItemStat, ItemStatAdmin)
admin.site.register(models.Ability)

