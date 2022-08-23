from django.contrib import admin
from .models import Branch


class BranchAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name_branch', 'opening_hours_start_branch', 'opening_hours_end_branch', 'address_branch', ]
    list_display_links = ['pk', 'name_branch', ]
    search_fields = ['name_branch', ]
    list_per_page = 50


admin.site.register(Branch, BranchAdmin)
