from django.contrib import admin
from .models import Address


class AddressAdmin(admin.ModelAdmin):
    list_display = ['pk', 'cep_address', 'street_address', 'district_address', 'number_address', ]
    list_display_links = ['pk', 'cep_address', ]
    list_filter = ['state_address', 'city_address', ]
    search_fields = ['cep_address', 'street_address', 'district_address', ]
    list_per_page = 200


admin.site.register(Address, AddressAdmin)
