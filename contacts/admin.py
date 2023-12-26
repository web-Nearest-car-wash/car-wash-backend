from django.contrib import admin

from .models import ContactsModel


class ContactsAdmin(admin.TabularInline):
    """Класс админки контактов."""

    model = ContactsModel
