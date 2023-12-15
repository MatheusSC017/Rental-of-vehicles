from django.contrib import admin
from .models import Address


class AddressAdmin(admin.ModelAdmin):
    list_display = ['pk', 'cep', 'street', 'district', 'number', ]
    list_display_links = ['pk', 'cep', ]
    list_filter = ['state', 'city', ]
    search_fields = ['cep', 'street', 'district', ]
    list_per_page = 200


admin.site.register(Address, AddressAdmin)
