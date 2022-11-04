from django.contrib import admin

from api.models import Item, Lot, RelatedProduct


class ItemAdmin(admin.ModelAdmin):
    list_display = ['db_id', 'code', 'type', 'created', 'modified']


class RelatedProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'gtin', 'trade_item_unit_descriptor', 'created', 'modified']
    search_fields = ['id', 'item__code', 'gtin', 'trade_item_unit_descriptor']
    raw_id_fields = ['item']


class LotAdmin(admin.ModelAdmin):
    list_display = ['id', 'amount', 'bbd', 'created', 'modified', 'item']
    raw_id_fields = ['item']


admin.site.register(Item, ItemAdmin)
admin.site.register(RelatedProduct, RelatedProductAdmin)
admin.site.register(Lot, LotAdmin)
