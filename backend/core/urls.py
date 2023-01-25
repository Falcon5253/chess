from .admin import chess_admin_site
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from user.views import GetUserView, ApiAuthToken
# from django.urls import include


urlpatterns = [
    path('admin/', chess_admin_site.urls),
    path('view/', GetUserView.as_view()),
    path('obtain-token/', ApiAuthToken.as_view()),
    # path('api-auth/', include('rest_framework.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)