from .admin import chess_admin_site
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', chess_admin_site.urls),
    # path('view/', )
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)