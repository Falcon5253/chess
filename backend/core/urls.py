from .admin import chess_admin_site
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from user.views import ProfileView, ApiAuthToken, RegisterUserView, LogoutView
from games.views import GameView
# from django.urls import include


urlpatterns = [
    path('admin/', chess_admin_site.urls),
    path('profile/', ProfileView.as_view()),
    path('obtain-token/', ApiAuthToken.as_view()),
    path('register/', RegisterUserView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('games/', GameView.as_view())
    # path('api-auth/', include('rest_framework.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)