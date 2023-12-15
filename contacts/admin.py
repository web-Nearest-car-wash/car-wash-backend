from django.contrib import admin

from .models import ContactsModel


class ContactsAdmin(admin.ModelAdmin):
    """Класс админки контактов."""

    list_display = ('id', 'carwash', 'address', 'phone')
    empty_value_display = '-пусто-'


admin.site.register(ContactsModel, ContactsAdmin)
