from .models import Game
from django.contrib import admin
from core.admin import chess_admin_site

@admin.register(Game, site=chess_admin_site)
class UserAdmin(admin.ModelAdmin):
    pass