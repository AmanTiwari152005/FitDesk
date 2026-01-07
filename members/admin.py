from django.contrib import admin
from .models import Member

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'phone',
        'package',
        'expiry_date',
        'gym'
    )
    list_filter = ('package', 'expiry_date')
    search_fields = ('name', 'phone')
