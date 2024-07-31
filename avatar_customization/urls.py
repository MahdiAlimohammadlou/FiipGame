from django.urls import path
from .views import ItemManagementView

urlpatterns = [
    path('items/', ItemManagementView.as_view(), name='item'),
]