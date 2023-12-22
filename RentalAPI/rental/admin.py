from django.contrib import admin
from .models import Insurance, Rental


class InsuranceAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', ]
    list_display_links = ['pk', 'title', ]
    search_fields = ['title', ]
    ordering = ['price', ]
    list_per_page = 50


class RentalAdmin(admin.ModelAdmin):
    list_display = ['pk', 'client', 'vehicle', 'status', 'total_cost', ]
    list_display_links = ['pk', 'client', ]
    list_filter = ['status', ]
    search_fields = ['client', 'vehicle', ]
    ordering = ['total_cost', 'rent_deposit', ]
    list_per_page = 200


admin.site.register(Insurance, InsuranceAdmin)
admin.site.register(Rental, RentalAdmin)
