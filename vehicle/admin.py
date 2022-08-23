from django.contrib import admin
from .models import Vehicle


class VehicleAdmin(admin.ModelAdmin):
    list_display = ['chassi_vehicle', 'license_plate_vehicle', 'type_vehicle', 'brand_vehicle', 'model_vehicle',
                    'year_manufacure_vehicle', 'model_year_vehicle', 'fuel_vehicle', ]
    list_display_links = ['chassi_vehicle', 'license_plate_vehicle', ]
    search_fields = ['chassi_vehicle', 'license_plate_vehicle', 'brand_vehicle', 'model_vehicle', ]
    list_filter = ['type_vehicle', 'fuel_vehicle', ]
    list_per_page = 50


admin.site.register(Vehicle, VehicleAdmin)
