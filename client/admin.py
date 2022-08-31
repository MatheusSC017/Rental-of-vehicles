from django.contrib import admin
from .models import Client


class ClientAdmin(admin.ModelAdmin):
    list_display = ['user_client', 'cpf_person', 'cnh_person', 'finance_client', 'address_person']
    list_display_links = ['user_client', 'cpf_person', ]
    search_fields = ['cpf_person', 'cnh_person', ]
    list_per_page = 200


admin.site.register(Client)
