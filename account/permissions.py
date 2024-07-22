from rest_framework.permissions import BasePermission
from .models import Player

class IsAuthenticatedWithApiKey(BasePermission):
    def has_permission(self, request, view):
        api_key = request.headers.get('API-KEY')
        if api_key:
            try:
                player = Player.objects.get(api_key=api_key)
                request.player = player
                return True
            except Player.DoesNotExist:
                return False
        return False
