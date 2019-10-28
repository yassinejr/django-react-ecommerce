from rest_framework import serializers

from .models import Product, Size
from profiles.models import FavoritesProducts


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    available = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail',
        lookup_field='slug'
    )

    class Meta:
        model = Product
        fields = ('id', 'slug', 'url', 'title', 'price', 'discount_price',
                  'discount_percent', 'photo_main', 'photo_1', 'available', 'available_count')

    def get_available(self, obj):
        return obj.available


class ProductDetailSerializer(serializers.ModelSerializer):
    is_favorite_product = serializers.SerializerMethodField()
    is_in_cart = serializers.SerializerMethodField()
    discount_percent = serializers.SerializerMethodField()
    available = serializers.SerializerMethodField()
    sizes = SizeSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'

    def get_available(self, obj):
        return obj.available

    def get_discount_percent(self, obj):
        return obj.discount_percent

    def get_is_favorite_product(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return FavoritesProducts.objects.check_product(user, obj.id)
        return False

    def get_is_in_cart(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return user.cart.items.filter(product=obj.id).exists()
        return False
