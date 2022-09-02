from django.contrib import admin
from .models import Insurance, Rental


class InsuranceAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title_insurance', ]
    list_display_links = ['pk', 'title_insurance', ]
    search_fields = ['title_insurance', ]
    ordering = ['price_insurance', ]
    list_per_page = 50


class RentalAdmin(admin.ModelAdmin):
    list_display = ['pk', 'client_rental', 'vehicle_rental', 'status_rental', 'total_cost_rental', ]
    list_display_links = ['pk', 'client_rental', ]
    list_filter = ['status_rental', ]
    search_fields = ['client_rental', 'vehicle_rental', ]
    ordering = ['total_cost_rental', 'rent_deposit_rental', ]
    list_per_page = 200


admin.site.register(Insurance, InsuranceAdmin)
admin.site.register(Rental, RentalAdmin)
