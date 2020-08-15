from django.contrib import admin

from personal.models import Symbol, Codal


@admin.register(Codal)
class CodalAdmin(admin.ModelAdmin):
    list_display = ['title', 'symbol', 'forosh', 'type']


@admin.register(Symbol)
class SymbolAdmin(admin.ModelAdmin):
    pass
