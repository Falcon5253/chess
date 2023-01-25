from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser, PermissionsMixin

class Manager(BaseUserManager):
    def create_user(self, email, username, password=None):
        user = self.model(
            email = self.normalize_email(email),
            username = username)

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
        )

        user.is_active = True
        user.is_superuser = True
        user.save()
        
        return user

class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(verbose_name='Электронная почта', max_length=255, unique=True)
    username = models.CharField(verbose_name='Имя', max_length=255)

    is_active = models.BooleanField(verbose_name='активирован', default=True)
    is_superuser = models.BooleanField(verbose_name='администратор', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = Manager() 
 
    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'