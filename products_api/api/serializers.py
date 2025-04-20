from api.models import Item, Lot, RelatedProduct, Session
from rest_framework import serializers


class AcceptFileSerializer(serializers.Serializer):
    """serializer class used to accept a file field"""

    product_feed = serializers.FileField()


class AcceptCodeSerializer(serializers.Serializer):
    """serializer class used to accept item code"""

    code = serializers.CharField(required=False)


class RelatedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatedProduct
        fields = ["gtin", "trade_item_unit_descriptor"]

    def create(self, validated_data):
        related_product = super().create(validated_data)
        return related_product


class ItemCreateSerializer(serializers.ModelSerializer):
    related_products = RelatedProductSerializer(required=False)
    type = serializers.CharField(required=False)

    class Meta:
        model = Item
        fields = "__all__"

    def to_internal_value(self, data):
        # 'edeka_article_number' comes as str or boolean, this is to change the boolean 'False' to null before saving
        if data.get("edeka_article_number", None) is False:
            data["edeka_article_number"] = None

        # Same with 'notes'
        if data.get("notes", None) is False:
            data["notes"] = None

        # The field `trade_item_descriptor` has to be transformed to `trade_item_unit_descriptor` if it exists in the data
        # before being stored in the DB.
        if "trade_item_descriptor" in data:
            data["trade_item_unit_descriptor"] = data.pop("trade_item_descriptor")

        # Validation will fail if 'type' is not present in the data because of unique_together constraint in the table
        data["type"] = None if not data.get("type", None) else data["type"]
        return data

    def create(self, validated_data):
        if "related_products" in validated_data:
            related_products_dicts = validated_data.pop("related_products")
            item = super().create(validated_data)
            for related_products_dict in related_products_dicts:
                related_products_dict["item"] = item
                self.fields["related_products"].create(related_products_dict)
        else:
            item = super().create(validated_data)
        return item


class LotCreateSerializer(serializers.ModelSerializer):
    item = ItemCreateSerializer()

    class Meta:
        model = Lot
        fields = "__all__"

    def create(self, validated_data):
        item_dict = validated_data.pop("item")
        if not Item.objects.filter(code=item_dict["code"], type=item_dict["type"]):
            item_instance = self.fields["item"].create(item_dict)
        else:
            item_instance = Item.objects.filter(
                code=item_dict["code"], type=item_dict["type"]
            ).first()
        validated_data["item"] = item_instance
        lot = super().create(validated_data)
        return lot


class SessionCreateSerializer(serializers.ModelSerializer):
    amounts = LotCreateSerializer(many=True)

    class Meta:
        model = Session
        fields = "__all__"

    def create(self, validated_data):
        lots = validated_data.pop("amounts")

        # adding the session to the session tables
        session = super().create(validated_data)

        # assigning the session to each dict
        for lot in lots:
            lot["session"] = session

        # no we have all the data to create the lots
        self.fields["amounts"].create(lots)
        return session


class ItemListSerializer(serializers.ModelSerializer):
    related_products = serializers.SerializerMethodField()
    amount_in_all_lots = serializers.SerializerMethodField()
    lots = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = [
            "code",
            "type",
            "amount_in_all_lots",
            "lots",
            "id",
            "brand",
            "description",
            "status",
            "categ_id",
            "category_id",
            "category",
            "amount_multiplier",
            "edeka_article_number",
            "gross_weight",
            "net_weight",
            "unit_name",
            "notes",
            "packaging",
            "related_products",
            "requires_best_before_date",
            "requires_meat_info",
            "trade_item_unit_descriptor",
            "trade_item_unit_descriptor_name",
            "validation_status",
            "regulated_name",
            "vat_rate",
            "vat",
            "hierarchies",
        ]

    def get_related_products(self, obj):
        related_products = obj.related_products.all()
        if related_products:
            return RelatedProductSerializer(related_products, many=True).data
        else:
            return

    def get_amount_in_all_lots(self, obj):
        amount_in_all_lots = 0
        [amount_in_all_lots := amount_in_all_lots + lot.amount for lot in obj.lot.all()]
        return amount_in_all_lots

    def get_lots(self, obj):
        return LotListSerializer(obj.lot.all(), many=True).data


class SessionListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Session
        fields = [
            "session_id",
            "session_start_time",
            "session_end_time",
            "supplier_id",
            "user_id",
        ]


class LotListSerializer(serializers.ModelSerializer):
    session = serializers.SerializerMethodField()

    class Meta:
        model = Lot
        fields = [
            "lot_number",
            "amount",
            "bbd",
            "comment",
            "country_of_disassembly",
            "country_of_rearing",
            "country_of_slaughter",
            "cutting_plant_registration",
            "slaughterhouse_registration",
            "session",
        ]

    def get_session(self, obj):
        return SessionListSerializer(obj.session).data
