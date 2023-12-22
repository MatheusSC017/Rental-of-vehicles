from django.contrib import admin
from .models import Vehicle, VehicleClassification


class VehicleClassificationAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'daily_cost', ]
    list_display_links = ['pk', 'title', ]
    search_fields = ['title', ]
    ordering = ['daily_cost', ]
    list_per_page = 50


class VehicleAdmin(admin.ModelAdmin):
    list_display = ['renavam', 'chassi', 'license_plate', 'type', 'brand',
                    'model', 'year_manufacture', 'model_year', 'fuel', ]
    list_display_links = ['renavam', 'chassi', 'license_plate', ]
    search_fields = ['renavam', 'chassi', 'license_plate', 'brand', 'model', ]
    list_filter = ['type', 'fuel', ]
    list_per_page = 100


admin.site.register(VehicleClassification, VehicleClassificationAdmin)
admin.site.register(Vehicle, VehicleAdmin)
