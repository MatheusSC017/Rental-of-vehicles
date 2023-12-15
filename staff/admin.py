from django.contrib import admin
from .models import StaffMember


class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'cpf', 'salary', 'address']
    list_display_links = ['user', 'cpf', ]
    search_fields = ['cpf', ]
    list_per_page = 200


admin.site.register(StaffMember, StaffMemberAdmin)
