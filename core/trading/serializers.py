from rest_framework import serializers

from trading.models import Offer


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = (
            'user',
            'item',
            'price',
            'order_type',
            'entity_quantity',
            'quantity',
            'is_active'
        )
