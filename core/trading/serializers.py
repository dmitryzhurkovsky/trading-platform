from rest_framework import serializers

from trading.models import Currency, Inventory, Item, Offer, Trade


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
        if data.get('order_type') == Offer.OrderType.BUY.value:
            if data.get('user').money < data.get('requested_quantity') * data.get('price'):
                raise serializers.ValidationError("You haven't enough money")

        elif data.get('order_type') == Offer.OrderType.SOLD.value:
            if Inventory.objects.get(
                    user=data.get('user'),
                    item=data.get('item')
            ).quantity < data.get('requested_quantity'):
                raise serializers.ValidationError("You haven't enough stocks")

        return data


class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = (
            'price',
            'currency',
            'details'
        )


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = (
            'code',
            'name'
        )


class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = (
            'item',
            'buyer',
            'seller',
            'quantity',
            'unit_price',
            'description',
            'buyer_offer',
            'seller_offer'
        )


class WatchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = (
            'item'
        )


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = (
            'item',
            'quantity'
        )
