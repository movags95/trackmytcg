from django.urls import path
from .views import UserSettingsViewSet

urlpatterns = [
    path('', UserSettingsViewSet.as_view({'get': 'list', 'put': 'update'}), name='user-settings'),
]
