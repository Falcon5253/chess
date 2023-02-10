from rest_framework import serializers
import math
from .models import Game


GAMEBOARD = [
    ['A8', 'B8', 'C8', 'D8', 'E8', 'F8', 'G8', 'H8'],
    ['A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7'],
    ['A6', 'B6', 'C6', 'D6', 'E6', 'F6', 'G6', 'H6'],
    ['A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5'],
    ['A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4'],
    ['A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3'],
    ['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2'],
    ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1'],
]

def get_figure_name_by_code(code):
    match code:
        case '1':
            return 'pawn-w'
        case '2':
            return 'rook-w'
        case '3':
            return 'knight-w'
        case '4':
            return 'bishop-w'
        case '5':
            return 'king-w'
        case '6':
            return 'queen-w'
        case '7':
            return 'pawn-b'
        case '8':
            return 'rook-b'
        case '9':
            return 'knight-b'
        case 'A':
            return 'bishop-b'
        case 'B':
            return 'king-b'
        case 'C':
            return 'queen-b'
        case _:
            return 'empty'

class GameDataField(serializers.Field):

    def to_representation(self, value):
        data = str(value)[2:-1]
        index = 0
        response_data = []
        for code in data:
            row = math.floor(index / 8)
            column = index % 8
            response_data.append({
                "cell": GAMEBOARD[row][column],
                "figure": get_figure_name_by_code(code),
            })
            
            index += 1
        return response_data

    def to_internal_value(self, data):
        return data

class GameSerializer(serializers.ModelSerializer):
    player1 = serializers.CharField()
    player2 = serializers.CharField()
    game_data = GameDataField()
    class Meta:
        model = Game
        fields = ['id', 'player1', 'player2', 'game_data']