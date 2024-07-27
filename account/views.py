# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import PlayerSerializer, PlayerCreateSerializer, BusinessSerializer, PlayerBusinessSerializer
from .models import Business, Player, PlayerBusiness

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

class ListBusinessesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        player = get_object_or_404(Player, user=request.user.id)
        player_businesses = PlayerBusiness.objects.filter(player=player)
        all_businesses = Business.objects.all()

        purchased_businesses_data = PlayerBusinessSerializer(player_businesses, many=True, context={'request': request}).data
        purchased_business_ids = [pb['business'] for pb in purchased_businesses_data]

        unpurchased_businesses = [b for b in all_businesses if b.id not in purchased_business_ids]
        unpurchased_businesses_data = BusinessSerializer(unpurchased_businesses, many=True, context={'request': request}).data

        return Response({
            'purchased_businesses': purchased_businesses_data,
            'unpurchased_businesses': unpurchased_businesses_data
        })

class BuyBusinessView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, business_id):
        player = get_object_or_404(Player, user=request.user.id)
        business = get_object_or_404(Business, id=business_id)
        success = player.buy_business(business)
        business_player_queryset = PlayerBusiness.objects.get(business=business_id, player=player)
        business_player_serializer = PlayerBusinessSerializer(business_player_queryset, context={"request":request}) 
        
        if success:
            return Response({
                'business_data': business_player_serializer.data,
                'success': success
            })
        return Response({
            'business_data': business_player_serializer.data,
            'success': success
        }, status=status.HTTP_400_BAD_REQUEST)

class UpgradeBusinessView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, business_id):
        player = get_object_or_404(Player, user=request.user.id)
        success = player.upgrade_business(business_id)
        business_player_queryset = PlayerBusiness.objects.get(business=business_id, player=player)
        business_player_serializer = PlayerBusinessSerializer(business_player_queryset, context={"request":request}) 

        if success:
            return Response({
                'business_data': business_player_serializer.data,
                'success': success
            })
        return Response({
            'business_data': business_player_serializer.data,
            'success': success
        }, status=status.HTTP_400_BAD_REQUEST)
