from .models import User
from django.contrib import admin
from core.admin import chess_admin_site

@admin.register(User, site=chess_admin_site)
class UserAdmin(admin.ModelAdmin):
    pass