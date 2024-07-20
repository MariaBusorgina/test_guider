from rest_framework import serializers

from .models import City, Shop, Street


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'title']


class StreetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Street
        fields = ['id', 'title']


class ShopSerializer(serializers.ModelSerializer):
    city = serializers.SerializerMethodField()
    street = serializers.SerializerMethodField()

    class Meta:
        model = Shop
        fields = ['id', 'title', 'city', 'street', 'house', 'open_time', 'close_time']

    def get_city(self, obj):
        return obj.city.title

    def get_street(self, obj):
        return obj.street.title


class ShopCreateSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(write_only=True)
    street_name = serializers.CharField(write_only=True)

    class Meta:
        model = Shop
        fields = ['title', 'city_name', 'street_name', 'house', 'open_time', 'close_time']

    def create(self, validated_data):
        city_name = validated_data.pop('city_name')
        street_name = validated_data.pop('street_name')

        city, _ = City.objects.get_or_create(title=city_name)
        street, _ = Street.objects.get_or_create(title=street_name, city=city)

        shop = Shop.objects.create(city=city, street=street, **validated_data)
        return shop
