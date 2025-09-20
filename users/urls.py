from django.urls import path
from .views import RegisterAPIView, LoginAPIView, PetListCreateAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('pets/', PetListCreateAPIView.as_view(), name='pets'),
]
