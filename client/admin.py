from django.contrib import admin
from .models import Client


class ClientAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user_client', 'cpf_client', 'cnh_client', 'finance_client', 'address_client']
    list_display_links = ['pk', 'user_client', 'cpf_client', ]
    search_fields = ['cpf_client', 'cnh_client', ]
    list_per_page = 50


admin.site.register(Client)
