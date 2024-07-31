from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from account.models import (Player, PlayerBusiness, PlayerCryptocurrency, PlayerProperty,
                             PlayerStock, PlayerVehicle,) 
from account.serializers import (PlayerBusinessSerializer, PlayerCryptocurrencySerializer,
                                 PlayerPropertySerializer, PlayerStockSerializer,
                                 PlayerVehicleSerializer,)
from .models import Business, Cryptocurrency, Stock, Property, Vehicle
from .serializers import (BusinessSerializer, CryptocurrencySerializer, PropertySerializer,
                           StockSerializer, VehicleSerializer)
from core.exceptions import NotEnoughMoney, InvalidQuantity

class BusinessView(APIView):
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

    def post(self, request):
        player = get_object_or_404(Player, user=request.user.id)
        business_id = request.data.get('business_id')
        business = get_object_or_404(Business, id=business_id)
        action = request.data.get('action')

        try:
            if action == 'buy':
                player.buy_business(business)
            elif action == 'upgrade':
                player.upgrade_business(business_id)
            else:
                return Response({"detail": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

            business_player_queryset = PlayerBusiness.objects.get(business=business_id, player=player)
            business_player_serializer = PlayerBusinessSerializer(business_player_queryset, context={"request": request})

            return Response(business_player_serializer.data, status=status.HTTP_201_CREATED)
        except NotEnoughMoney as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except InvalidQuantity as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CryptocurrencyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        player = get_object_or_404(Player, user=request.user.id)
        player_cryptocurrencies = PlayerCryptocurrency.objects.filter(player=player)
        all_cryptocurrencies = Cryptocurrency.objects.all()

        purchased_cryptocurrencies_data = PlayerCryptocurrencySerializer(player_cryptocurrencies, many=True, context={'request': request}).data
        purchased_cryptocurrency_ids = [pc['cryptocurrency'] for pc in purchased_cryptocurrencies_data]

        unpurchased_cryptocurrencies = [c for c in all_cryptocurrencies if c.id not in purchased_cryptocurrency_ids]
        unpurchased_cryptocurrencies_data = CryptocurrencySerializer(unpurchased_cryptocurrencies, many=True, context={'request': request}).data

        return Response({
            'purchased_cryptocurrencies': purchased_cryptocurrencies_data,
            'unpurchased_cryptocurrencies': unpurchased_cryptocurrencies_data
        })

    def post(self, request):
        player = get_object_or_404(Player, user=request.user.id)
        cryptocurrency_id = request.data.get('cryptocurrency_id')
        cryptocurrency = get_object_or_404(Cryptocurrency, id=cryptocurrency_id)
        action = request.data.get('action')
        quantity = request.data.get('quantity')

        try:
            if action == 'buy':
                player.buy_cryptocurrency(cryptocurrency, quantity)
                return Response({"detail": "Cryptocurrency purchased successfully"}, status=status.HTTP_200_OK)
            elif action == 'sell':
                player.sell_cryptocurrency(cryptocurrency, quantity)
                return Response({"detail": "Cryptocurrency sold successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)
        except NotEnoughMoney as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except InvalidQuantity as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class PropertyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        player = get_object_or_404(Player, user=request.user.id)
        player_properties = PlayerProperty.objects.filter(player=player)
        all_properties = Property.objects.all()

        purchased_properties_data = PlayerPropertySerializer(player_properties, many=True, context={'request': request}).data
        purchased_property_ids = [pp['property'] for pp in purchased_properties_data]

        unpurchased_properties = [p for p in all_properties if p.id not in purchased_property_ids]
        unpurchased_properties_data = PropertySerializer(unpurchased_properties, many=True, context={'request': request}).data

        return Response({
            'purchased_properties': purchased_properties_data,
            'unpurchased_properties': unpurchased_properties_data
        })

    def post(self, request):
        player = get_object_or_404(Player, user=request.user.id)
        property_id = request.data.get('property_id')
        property = get_object_or_404(Property, id=property_id)
        action = request.data.get('action')

        try:
            if action == 'buy':
                player.buy_property(property)
                return Response({"detail": "Property purchased successfully"}, status=status.HTTP_200_OK)
            elif action == 'sell':
                player.sell_property(property)
                return Response({"detail": "Property sold successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)
        except NotEnoughMoney as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except InvalidQuantity as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class StockView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        player = get_object_or_404(Player, user=request.user.id)
        player_stocks = PlayerStock.objects.filter(player=player)
        all_stocks = Stock.objects.all()

        purchased_stocks_data = PlayerStockSerializer(player_stocks, many=True, context={'request': request}).data
        purchased_stock_ids = [ps['stock'] for ps in purchased_stocks_data]

        unpurchased_stocks = [s for s in all_stocks if s.id not in purchased_stock_ids]
        unpurchased_stocks_data = StockSerializer(unpurchased_stocks, many=True, context={'request': request}).data

        return Response({
            'purchased_stocks': purchased_stocks_data,
            'unpurchased_stocks': unpurchased_stocks_data
        })

    def post(self, request):
        player = get_object_or_404(Player, user=request.user.id)
        stock_id = request.data.get('stock_id')
        stock = get_object_or_404(Stock, id=stock_id)
        action = request.data.get('action')
        quantity = request.data.get('quantity')

        try:
            if action == 'buy':
                player.buy_stock(stock, quantity)
                return Response({"detail": "Stock purchased successfully"}, status=status.HTTP_200_OK)
            elif action == 'sell':
                player.sell_stock(stock, quantity)
                return Response({"detail": "Stock sold successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)
        except NotEnoughMoney as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except InvalidQuantity as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class VehicleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        player = get_object_or_404(Player, user=request.user.id)
        player_vehicles = PlayerVehicle.objects.filter(player=player)
        all_vehicles = Vehicle.objects.all()

        purchased_vehicles_data = PlayerVehicleSerializer(player_vehicles, many=True, context={'request': request}).data
        purchased_vehicle_ids = [pv['vehicle'] for pv in purchased_vehicles_data]

        unpurchased_vehicles = [v for v in all_vehicles if v.id not in purchased_vehicle_ids]
        unpurchased_vehicles_data = VehicleSerializer(unpurchased_vehicles, many=True, context={'request': request}).data

        return Response({
            'purchased_vehicles': purchased_vehicles_data,
            'unpurchased_vehicles': unpurchased_vehicles_data
        })

    def post(self, request):
        player = get_object_or_404(Player, user=request.user.id)
        vehicle_id = request.data.get('vehicle_id')
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        action = request.data.get('action')

        try:
            if action == 'buy':
                player.buy_vehicle(vehicle)
                return Response({"detail": "Vehicle purchased successfully"}, status=status.HTTP_200_OK)
            elif action == 'sell':
                player.sell_vehicle(vehicle)
                return Response({"detail": "Vehicle sold successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)
        except NotEnoughMoney as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except InvalidQuantity as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)