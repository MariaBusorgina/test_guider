from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import City, Street, Shop
from .serializers import CitySerializer, ShopSerializer, ShopCreateSerializer


class CityListAPIView(generics.ListAPIView):
    """
    Представление для получения списка городов или списка улиц указанного города.
     - GET /city/ : Возвращает список всех городов.
    - GET /city/{city_id}/street/ : Возвращает список всех улиц указанного города (city_id — идентификатор города).
    """
    serializer_class = CitySerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if not pk:
            return City.objects.all()
        return Street.objects.filter(city=pk)


class ShopAPIView(APIView):
    """
    Представление для получения списка магазинов и создания нового магазина.
    """
    def get(self, request):
        """
        Обрабатывает GET запрос для получения списка магазинов.

        Параметры запроса:
            - street (необязательно): Фильтрация по названию улицы.
            - city (необязательно): Фильтрация по названию города.
            - open (необязательно): Фильтрация по статусу открытости (0 - закрыт, 1 - открыт).
        """
        street = request.query_params.get('street')
        city = request.query_params.get('city')
        open_status = request.query_params.get('open')

        shops = Shop.objects.all()

        if street:
            shops = shops.filter(street__title__icontains=street)

        if city:
            shops = shops.filter(city__title__icontains=city)

        if open_status is not None:
            if open_status == '1':
                open_shops = [shop for shop in shops if shop.is_open()]
                serializer = ShopSerializer(open_shops, many=True)
            elif open_status == '0':
                closed_shops = [shop for shop in shops if not shop.is_open()]
                serializer = ShopSerializer(closed_shops, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = ShopSerializer(shops, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Обрабатывает POST запрос для создания нового магазина.
        Запрос должен содержать JSON объект с данными магазина.
        Если город и улица не существуют, они будут созданы.
        """
        serializer = ShopCreateSerializer(data=request.data)
        if serializer.is_valid():
            shop = serializer.save()
            return Response({'id': shop.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








