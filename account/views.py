# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from .models import Player, Business
from .serializers import PlayerSerializer, PlayerCreateSerializer
from .permissions import IsAuthenticatedWithApiKey

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
    permission_classes = [IsAuthenticatedWithApiKey]

    def post(self, request, *args, **kwargs):
        serializer = PlayerCreateSerializer(data=request.data)
        if serializer.is_valid():
            player = serializer.save()
            response_data = serializer.data
            response_data['api_key'] = player.api_key
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        player = request.player
        serializer = PlayerSerializer(player)
        return Response(serializer.data, status=status.HTTP_200_OK)

class BuyBusinessView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedWithApiKey]
    serializer_class = PlayerSerializer

    def post(self, request, *args, **kwargs):
        player = request.player
        business = Business.objects.get(id=request.data['business_id'])
        if player.buy_business(business):
            return Response({'detail': 'Business bought successfully'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Not enough coins'}, status=status.HTTP_400_BAD_REQUEST)

class UpgradeBusinessView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedWithApiKey]
    serializer_class = PlayerSerializer

    def post(self, request, *args, **kwargs):
        player = request.player
        business_id = request.data['business_id']
        if player.upgrade_business(business_id):
            return Response({'detail': 'Business upgraded successfully'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Not enough coins or business not found'}, status=status.HTTP_400_BAD_REQUEST)
