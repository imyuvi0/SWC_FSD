from rest_framework import serializers
from .models import Game, Publisher, Order, OrderItem


class GameSerializer(serializers.ModelSerializer):
    available = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = ('id', 'title', 'publisher', 'price', 'available')
        read_only_fields = ('publisher',)

    def get_available(self, obj):
        return obj.gamekey_set.filter(status='active', owner__isnull=True).exists()


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        exclude = ('webhook_secret',)


class OrderItemSerializer(serializers.ModelSerializer):
    game_title = serializers.CharField(source='game.title', read_only=True)
    key_string = serializers.CharField(source='game_key.key_string', read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'game', 'game_title', 'key_string', 'price')


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    buyer_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'buyer_username', 'total_amount', 'created_at', 'items')
