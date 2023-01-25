from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from .models import User
from rest_framework.authtoken.models import Token
from .serializers import LoginUserSerializer, RegisterUserSerializer

class GetUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),
            'auth': str(request.auth),
        }
        return Response(content)

class RegisterUserView(APIView):
    serializer_class = RegisterUserSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'true'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        token_key = request.headers.get('Authorization')[7:] # getting token from request header
        
        token = Token.objects.filter(key=token_key)
        token.delete()
        data = {
            'success': 'true'
        }
        return Response(data)
    
    
class ApiAuthToken(ObtainAuthToken):
    serializer_class = LoginUserSerializer
