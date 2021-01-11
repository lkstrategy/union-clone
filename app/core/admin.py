from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from core import models


class UserAdmin(BaseUserAdmin):
    ordering=['id']
    list_display=['email','name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Infor'), {'fields': ('name',)}),
        (
            ('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_client',)}
        ),
        ( ('Important Dates'), {'fields': ('last_login',)}),
        ( ('Client'), {'fields': ('client',)}),

    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Client)
admin.site.register(models.Lead)
admin.site.register(models.LeadComplete)
admin.site.register(models.CompanyLead)
admin.site.register(models.Engagement)
admin.site.register(models.ClientLeadScore)
admin.site.register(models.Message)
admin.site.register(models.NewsArticles)

