from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from .models import User, Manager

class LoginUserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(
        label=_("Email"),
        write_only=True,
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
    
    class Meta:
        model = User
        fields = ['email', 'password', 'token']
        
class RegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        label=_("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    username = serializers.CharField(
        label=_('Username'),
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )
    
    def validate_email(self, value):
        user_check = User.objects.filter(email=value)
        if len(user_check) > 0:
            raise serializers.ValidationError('Почта уже занята')
        return value
        
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        username = attrs.get('username')
        if email and password and username:
            if len(username) > 16:
                msg = _('Nickname is too long. It has to be not bigget than 16 characters')
                raise serializers.ValidationError(msg, code='registration')

        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='registration')

        return attrs

    def save(self, **kwargs):
        data = self.initial_data
        email = data['email']
        username = data['username']
        password = data['password']
        
        user = User(
            email = Manager.normalize_email(email),
            username = username)
        
        user.set_password(password)
        user.save()
        return user
    
    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'token']