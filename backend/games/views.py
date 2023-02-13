from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Game
from .serializers import GameSerializer
from core.pusher import pusher_client

whites = ['1', '2', '3', '4', '5', '6']
blacks =['7', '8', '9', 'A', 'B', 'C']

indexes = {
    'A': 0,
    'B': 1,
    'C': 2,
    'D': 3,
    'E': 4,
    'F': 5,
    'G': 6,
    'H': 7,
    '1': 0,
    '2': 1,
    '3': 2,
    '4': 3,
    '5': 4,
    '6': 5,
    '7': 6,
    '8': 7
}


def game_data_to_array(game_data):
    game_data = game_data.decode('ascii')
    game_array = ['']
    for index, figure in enumerate(game_data):
        if index % 8 == 0 and index != 0:
            game_array.insert(0, '')
        
        game_array[0] += figure

    return game_array

def turn_to_coordinates(turn):
    turn_from = turn[0:2]
    turn_to = turn[3:5]
    
    x1 = turn_from[0]
    y1 = turn_from[1]
    x2 = turn_to[0]
    y2 = turn_to[1]
    
    x1 = indexes[x1]
    x2 = indexes[x2]
    y1 = indexes[y1]
    y2 = indexes[y2]
    return x1, x2, y1, y2

def move_by_coordinates(game_array, x1, x2, y1, y2):
    # Copying data from previous position to the new one
    game_array[y2] = game_array[y2][:x2] + game_array[y1][x1] + game_array[y2][x2+1:]
    
    # Clearing data at the prevous position
    game_array[y1] = game_array[y1][:x1] + '0' + game_array[y1][x1+1:]
    
    # Returning new array
    return game_array


def game_array_to_data(game_array):
    string_of_game_data = ''
    for line in game_array:
        string_of_game_data = line + string_of_game_data
        
    game_data = bytes(string_of_game_data, 'ascii')
    
    return  game_data


def make_turn(user, game: Game, turn: str):
    # Getting current board data
    game_array = game_data_to_array(game.game_data)
    # Parsing turn from where to where put a figure
    x1, x2, y1, y2 = turn_to_coordinates(turn)
    next_step_game_array = move_by_coordinates(game_array, x1, x2, y1, y2)
    
    game_data = game_array_to_data(next_step_game_array)
    game.game_data = game_data
    game.turn_of_white = not(game.turn_of_white)
    game.save()
    game_data = GameSerializer(game)
    return game_data.data

def check_hack(figure, next_field_value):
    if next_field_value == '0':
        return False
    
    if (figure in whites and next_field_value in blacks) or (figure in blacks and next_field_value in whites):
        return True
    
    return 'Friendly fire!'
        


def check_turn_posibility(figure, is_hack, x1, x2, y1, y2):
    # Если фигура белая пешка
    print(x1, y1)
    print(x2, y2)
    match figure:
        
        case '1':
            # Если атакует фигуру оппонента
            if is_hack:
                
                
                # Считаем смещение, координата "x" по модулю
                x = abs(x2 - x1)
                y = y2 - y1
                
                # Обе координаты должны отличаться на единицу
                if x == 1 and y == 1:
                    return True
                return False
            
            # Если не атакует
            else:
                # Считаем смещение
                x = x2 - x1
                y = y2 - y1
                print(x, y)
                
                
                # Координата "x" не должна меняться
                if x == 0:
                    # Если проходит через вражеское поле
                    if y2 > 3:
                        # Переместиться можно на одну клетку
                        if y == 1:
                            return True
                        return False
                    
                    
                    # Если не проходит вражеское
                    # Переместиться можно на растояние до двух клеток    
                    if y < 3 and y > 0:
                        return True
                    
                    return False
                return False

        case _:
            return True


def turn_is_valid(game: Game, turn):
    print(turn)
    x1, x2, y1, y2 = turn_to_coordinates(turn)
    game_data = game_data_to_array(game.game_data)
    figure = game_data[y1][x1]
    is_hack = check_hack(figure, game_data[y2][x2])
    
    if is_hack == 'Friendly fire!':
        return False
    
    if check_turn_posibility(figure, is_hack, x1, x2, y1, y2):
        return True
    
    return False
    
    
    
    

class GameView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['post', 'get']
    
    def get(self, request, format=None):
        games = Game.objects.all()
        ser = GameSerializer(games, many=True)
        return Response(ser.data)
    
    def post(self, request):
        data = request.POST
        id = data['game_id']
        
        turn = data['turn']
        game = Game.objects.get(id=id)
        user = request.user
        
        if not(turn_is_valid(game, turn)):
            return Response({'success':'false'})
        
        new_game_data = make_turn(user, game, turn)
        pusher_client.trigger('game' + str(id), 'turnWasMade', new_game_data)
        
        # Пусть респонс возвращает сразу make_turn
        # Еще надо добавить сохранение сего действа в БД
        return Response({'success':'true'})