from rest_framework import serializers
from .models import Game


class BinaryField(serializers.Field):

    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        return data

class GameSerializer(serializers.ModelSerializer):
    player1 = serializers.CharField()
    player2 = serializers.CharField()
    game_data = BinaryField()
    class Meta:
        model = Game
        fields = ['player1', 'player2', 'game_data']