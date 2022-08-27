from django.contrib import admin
from .models import Client


class ClientAdmin(admin.ModelAdmin):
    list_display = ['user_client', 'cpf_client', 'cnh_client', 'finance_client', 'address_client']
    list_display_links = ['user_client', 'cpf_client', ]
    search_fields = ['cpf_client', 'cnh_client', ]
    list_per_page = 200


admin.site.register(Client)
