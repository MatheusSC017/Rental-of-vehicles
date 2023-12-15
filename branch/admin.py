from django.contrib import admin
from .models import Branch


class BranchAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'opening_hours_start', 'opening_hours_end', 'address', ]
    list_display_links = ['pk', 'name', ]
    search_fields = ['name', ]
    list_per_page = 50


admin.site.register(Branch, BranchAdmin)
