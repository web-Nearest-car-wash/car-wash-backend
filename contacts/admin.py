from django.contrib import admin

from .models import Contacts


class ContactsAdmin(admin.ModelAdmin):
    """Класс контактов."""

    list_display = ('id', 'carwash', 'address', 'phone')
    empty_value_display = '-пусто-'


admin.site.register(Contacts, ContactsAdmin)
