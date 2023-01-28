from user.models import User
from django.db import models

class Game(models.Model):
    player1 = models.ForeignKey(
        User,
        related_name='player1',
        on_delete=models.CASCADE,
    )
    player2 = models.ForeignKey(
        User,
        related_name='player2',
        on_delete=models.CASCADE,
    )
    game_data = models.BinaryField(
        null=True,
        name='Игровые данные'
    )
    history = models.BinaryField(
        null=True,
        name='История ходов'
    )
    
    def __str__(self):
        return f'{self.player1.username} против {self.player2.username} (#' + str(self.id) + ')'