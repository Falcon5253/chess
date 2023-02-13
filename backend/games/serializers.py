from rest_framework import serializers
from math import floor
from .models import Game


whites = ['1', '2', '3', '4', '5', '6']
blacks =['7', '8', '9', 'A', 'B', 'C']

GAMEBOARD = [
    ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1'],
    ['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2'],
    ['A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3'],
    ['A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4'],
    ['A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5'],
    ['A6', 'B6', 'C6', 'D6', 'E6', 'F6', 'G6', 'H6'],
    ['A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7'],
    ['A8', 'B8', 'C8', 'D8', 'E8', 'F8', 'G8', 'H8'],
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

def game_data_to_array(game_data):
    game_data = game_data.decode('ascii')
    game_array = ['']
    for index, figure in enumerate(game_data):
        if index % 8 == 0 and index != 0:
            game_array.insert(0, '')
        
        game_array[0] += figure

    return game_array

def calc_turns(game_data, x, y):
    game_data = game_data_to_array(game_data)
    figure = game_data[y][x]
    turns = []
    match figure:
        # Getting turns
        
        # For white pawns
        case "1":
            # Adding pawn going forwards
            if y < 7:
                if game_data[y+1][x] == '0':
                    turns.append(GAMEBOARD[y+1][x])
                    if y < 2 and game_data[y+2][x] == '0':
                        turns.append(GAMEBOARD[y+2][x])
                
                # Checking hack posibility
                if x != 7:
                    if game_data[y+1][x+1] in blacks:
                        turns.append(GAMEBOARD[y+1][x+1])
                if x != 0:
                    if game_data[y+1][x-1] in blacks:
                        turns.append(GAMEBOARD[y+1][x-1])
                
            return turns
        
        # For others
        case _:
            return []
    
    

class GameDataField(serializers.Field):

    def to_representation(self, value):
        data = str(value)[2:-1]
        index = 0
        response_data = []
        for code in data:
            row = abs(floor(index / 8) - 7)
            column = index % 8
            response_data.append({
                "cell": GAMEBOARD[row][column],
                "figure": get_figure_name_by_code(code),
                "turns": calc_turns(value, column, row)
            })
            
            index += 1
        return response_data

    def to_internal_value(self, data):
        return data


class GameSerializer(serializers.ModelSerializer):
    player1 = serializers.CharField()
    player2 = serializers.CharField()
    game_data = GameDataField()
    whose_turn = serializers.SerializerMethodField('turn_of')

    def turn_of(self, obj):
        if obj.turn_of_white:
            return obj.player1.email
        return obj.player2.email
        
    class Meta:
        model = Game
        fields = ['id', 'player1', 'player2', 'game_data', 'whose_turn']