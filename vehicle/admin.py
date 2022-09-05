from django.contrib import admin
from .models import Vehicle, VehicleClassification


class VehicleClassificationAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title_classification', 'daily_cost_classification', ]
    list_display_links = ['pk', 'title_classification', ]
    search_fields = ['title_classification', ]
    ordering = ['daily_cost_classification', ]
    list_per_page = 50


class VehicleAdmin(admin.ModelAdmin):
    list_display = ['renavam_vehicle', 'chassi_vehicle', 'license_plate_vehicle', 'type_vehicle', 'brand_vehicle',
                    'model_vehicle', 'year_manufacture_vehicle', 'model_year_vehicle', 'fuel_vehicle', ]
    list_display_links = ['renavam_vehicle', 'chassi_vehicle', 'license_plate_vehicle', ]
    search_fields = ['renavam_vehicle', 'chassi_vehicle', 'license_plate_vehicle', 'brand_vehicle', 'model_vehicle', ]
    list_filter = ['type_vehicle', 'fuel_vehicle', ]
    list_per_page = 100


admin.site.register(VehicleClassification, VehicleClassificationAdmin)
admin.site.register(Vehicle, VehicleAdmin)
