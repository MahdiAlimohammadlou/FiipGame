# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Player
from .serializers import PlayerSerializer

@api_view(['GET'])
def top_players(request):
    try:
        level = request.query_params.get('level')
        if level is not None:
            try:
                level = int(level)
            except ValueError:
                return Response({'detail': 'Level must be an integer'}, status=status.HTTP_400_BAD_REQUEST)
            players = Player.objects.filter(level=level).order_by('-coin')[:100]
        else:
            players = Player.objects.order_by('-coin')[:100]
        
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def player_by_device_id(request, device_id):
    try:
        player = Player.objects.get(device_id=device_id)
        serializer = PlayerSerializer(player)
        return Response(serializer.data)
    except Player.DoesNotExist:
        return Response({'detail': 'Player not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
