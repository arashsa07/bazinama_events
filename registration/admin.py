from django.contrib import admin
from django.db.models import Count
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import User, State, City, UserProfile


class UserProfileIsPaidListFilter(admin.SimpleListFilter):
    title = 'Is Paid'
    parameter_name = 'is_paid'

    def lookups(self, request, model_admin):
        return (
            ('0', 'No'),
            ('1', 'Yes')
        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.annotate(paid_count=Count('user__payment')).filter(paid_count=0)
        if self.value() == '1':
            return queryset.annotate(paid_count=Count('user__payment')).filter(paid_count__gt=0)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('nick_name', 'clash_id', 'cup_numbers', 'level', 'email', 'phone', 'birthday', 'gender', 'city', 'paid')
    list_filter = (UserProfileIsPaidListFilter, )
    readonly_fields = ('user', 'phone')

    def paid(self, obj):
        if obj.user.payment_set.filter(paid_status=True):
            return '<img src = "/static/admin/img/icon-yes.svg" alt="True">'
        return '<img src = "/static/admin/img/icon-no.svg" alt="False">'

    def phone(self, obj):
        return obj.user.phone_number

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    paid.allow_tags = True


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
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(City, CityAdmin)
