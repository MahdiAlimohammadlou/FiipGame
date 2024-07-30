from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Player, PlayerBusiness
from .serializers import PlayerSerializer, PlayerCreateSerializer, PlayerBusinessSerializer
from asset.models import Business
from asset.serializers import BusinessSerializer

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
    
class PlayerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PlayerCreateSerializer(data=request.data)
        if serializer.is_valid():
            player = serializer.save(user = request.user.id)
            return Response({"detail": "Player created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        player = Player.objects.get(user=request.user.id)
        serializer = PlayerSerializer(player)
        return Response(serializer.data, status=status.HTTP_200_OK)