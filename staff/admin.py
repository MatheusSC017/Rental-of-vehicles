from django.contrib import admin
from .models import StaffMember


class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ['user_staffmember', 'cpf_person', 'cnh_person', 'salary_staffmember', 'address_person']
    list_display_links = ['user_staffmember', 'cpf_person', ]
    search_fields = ['cpf_person', 'cnh_person', ]
    list_per_page = 200


admin.register(StaffMember)
