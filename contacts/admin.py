from django.contrib import admin

from .models import ContactsModel


class ContactsAdmin(admin.ModelAdmin):
    """Класс админки контактов."""

    list_display = ('carwash', 'address', 'phone', 'website')
    empty_value_display = '-пусто-'


admin.site.register(ContactsModel, ContactsAdmin)
