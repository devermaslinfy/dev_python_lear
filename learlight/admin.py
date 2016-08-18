from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from learlight.models import Account, JewelryType, Customer, Associate


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    pass


@admin.register(JewelryType)
class JewelryTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    readonly_fields = ('formatted_transaction_id', 'quote_id', )


class AssociateInline(admin.StackedInline):
    model = Associate
    can_delete = False
    verbose_name_plural = 'associate'


class UserAdmin(UserAdmin):
    inlines = (AssociateInline, )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
