from django.urls import path

from .views import CityListAPIView, ShopAPIView

urlpatterns = [
    path('city/', CityListAPIView.as_view(), name='city-list'),
    path('city/<int:pk>/street/', CityListAPIView.as_view(), name='street-list'),
    path('shop/', ShopAPIView.as_view(), name='shop-list-create'),

]