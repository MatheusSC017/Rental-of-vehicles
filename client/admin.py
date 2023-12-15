from django.contrib import admin
from .models import Client


class ClientAdmin(admin.ModelAdmin):
    list_display = ['user', 'cpf', 'cnh', 'finance', 'address']
    list_display_links = ['user', 'cpf', ]
    search_fields = ['cpf', 'cnh', ]
    list_per_page = 200


admin.site.register(Client)
