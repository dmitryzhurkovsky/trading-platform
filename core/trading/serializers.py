from rest_framework import serializers

from trading.models import (
    Offer,
    Item,
    Currency,
    Trade,
    Inventory
)


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = (
            'user',
            'item',
            'price',
            'order_type',
            'requested_quantity',
            'is_active'
        )

    def validate(self, data):
        if data.get('order_type') == 'b':
            if data.get('user').money < data.get('requested_quantity') * data.get('price'):
                raise serializers.ValidationError('You haven\'t enough money')

        elif data.get('order_type') == 's':
            if Inventory.objects.get(
                user=data.get('user'),
                item=data.get('item')
            ).quantity < data.get('requested_quantity'):
                raise serializers.ValidationError('You haven\'t enough stocks')

        return data


class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        exclude = ('id', )


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        exclude = ('id', )


class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        exclude = ('id', )


class WatchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        exclude = ('id', )


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        exclude = ('id', )