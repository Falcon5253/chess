from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Game
from .serializers import GameSerializer

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
            game_array.append('')
        
        game_array[-1] += figure

    return game_array

def turn_to_coordinates(turn):
    turn_from = turn[0:2]
    turn_to = turn[3:5]
    x1 = turn_from[1]
    y1 = turn_from[0]
    x2 = turn_to[1]
    y2 = turn_to[0]
    x1 = indexes[x1]
    x2 = indexes[x2]
    y1 = indexes[y1]
    y2 = indexes[y2]
    return x1, x2, y1, y2

def transfer_by_coordinates(game_array, x1, x2, y1, y2):
    # Copying data from previous position to the new one
    game_array[x2] = game_array[x2][:y2] + game_array[x1][y1] + game_array[x2][y2+1:]
    
    # Clearing data at the prevous position
    game_array[x1] = game_array[x1][:y1] + '0' + game_array[x1][y1+1:]
    
    # Returning new array
    return game_array


def make_turn(user, game, turn):
    # Getting current board data
    game_array = game_data_to_array(game.game_data)
    
    # Parsing turn from where to where put a figure
    x1, x2, y1, y2 = turn_to_coordinates(turn)
    for line in game_array:
        print(line)
    
    next_game_array = transfer_by_coordinates(game_array, x1, x2, y1, y2)

    for line in next_game_array:
        print(line)
    

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

        make_turn(user, game, turn)
        
        # Пусть респонс возвращает сразу make_turn
        # Еще надо добавить сохранение сего действа в БД
        return Response({'success':'true'})