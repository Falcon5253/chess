from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from .models import Game
from rest_framework.authtoken.models import Token
from .serializers import GameSerializer

class GameView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        games = Game.objects.all()
        ser = GameSerializer(games, many=True)
        return Response(ser.data)