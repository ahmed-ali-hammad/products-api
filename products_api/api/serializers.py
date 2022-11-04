from rest_framework import serializers

from api.models import Item, Lot, RelatedProduct


class RelatedProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = RelatedProduct
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        related_product = super().create(validated_data)
        return related_product

class ItemSerializer(serializers.Serializer):
    product_feed = serializers.FileField


class ItemCreateSerializer(serializers.ModelSerializer):
    related_products = RelatedProductSerializer(required=False)
    type = serializers.CharField(required=False)

    class Meta:
        model = Item
        fields = '__all__'

    def to_internal_value(self, data):
        # 'edeka_article_number' comes as str or boolean, this is to change the boolean 'False' to null before saving 
        if data.get('edeka_article_number', None) is False:
            data['edeka_article_number'] = None
        # Same with 'notes'
        if data.get('notes', None) is False:
            data['notes'] = None

        if 'trade_item_descriptor' in data:
            data['trade_item_unit_descriptor'] = data.pop('trade_item_descriptor')

        # Validation will fail if 'type' is not present in the data because of unique_together constraint in the table
        data['type'] = None if not data.get('type', None) else data['type']
        return data

    def create(self, validated_data):
        if 'related_products' in validated_data:
            related_products = validated_data.pop('related_products')
            item = super().create(validated_data)
            if len(related_products) > 0:
                for related_product in related_products:
                    related_product['item'] = item
                    print(related_product)
                    self.fields['related_products'].create(related_product)
        else:
            item = super().create(validated_data)
        return item


class LotSerializer(serializers.ModelSerializer):
    item = ItemCreateSerializer()

    class Meta:
        model = Lot
        fields = '__all__'

    def create(self, validated_data):
        item = validated_data.pop('item')
        if not Item.objects.filter(code=item['code'], type=item['type']):
            item = self.fields['item'].create(item)
        else:
            item = Item.objects.filter(code=item['code'], type=item['type']).first()
        validated_data['item'] = item
        lot = super().create(validated_data)
        return lot


class RelatedProductSerializer(serializers.ModelSerializer):
    item = ItemCreateSerializer()

    class Meta:
        model = RelatedProduct
        fields = '__all__'
