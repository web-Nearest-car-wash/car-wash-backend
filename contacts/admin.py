from django.contrib import admin

from .models import ContactsModel


class ContactsInline(admin.TabularInline):
    """Класс админки контактов."""

    model = ContactsModel
