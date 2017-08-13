from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import User, State, City


class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone_number', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'phone_number', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'phone_number', 'email', 'is_staff')
    search_fields = ('username', 'phone_number')


class StateAdmin(admin.ModelAdmin):
    list_display = ['state_name', ]
    list_filter = ['state_name', ]


class CityAdmin(admin.ModelAdmin):
    list_display = ['state', 'city_name']
    list_filter = ['state', ]
    ordering = ['state', ]


admin.site.register(User, MyUserAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(City, CityAdmin)
