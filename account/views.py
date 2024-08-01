import time
import hmac
import hashlib
import json

from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Player
from .serializers import PlayerSerializer, PlayerCreateSerializer

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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def tap_count(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        count = data.get('count')
        timestamp = int(request.headers.get('X-Tap-Timestamp'))
        signature = request.headers.get('X-Tap-Signature')

        if not timestamp or not signature:
            return Response({'error': 'Missing signature or timestamp'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate timestamp (e.g., within the last 60 seconds)
        if abs(time.time() - timestamp) > 60:
            return Response({'error': 'Invalid timestamp'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate signature
        expected_signature = hmac.new(
            settings.SECRET_KEY.encode(),
            f'{count}{timestamp}'.encode(),
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(expected_signature, signature):
            return Response({'error': 'Invalid signature'}, status=status.HTTP_400_BAD_REQUEST)

        player = get_object_or_404(Player, user=request.user.id)
        coin = player.multitap * count
        player.coin += coin 
        player.save()
        return Response({'success': True})

    return Response({'error': 'Invalid method'}, status=405)