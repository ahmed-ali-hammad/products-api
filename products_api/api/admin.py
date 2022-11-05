from api.models import Item, Lot, RelatedProduct, Session
from django.contrib import admin


class ItemAdmin(admin.ModelAdmin):
    list_display = ['db_id', 'code', 'type', 'created', 'modified']


class RelatedProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'gtin', 'trade_item_unit_descriptor', 'created', 'modified']
    search_fields = ['id', 'item__code', 'gtin', 'trade_item_unit_descriptor']
    raw_id_fields = ['item']


class LotAdmin(admin.ModelAdmin):
    list_display = ['id', 'amount', 'bbd', 'created', 'modified', 'item']
    raw_id_fields = ['item']


class SessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'session_id']


admin.site.register(Item, ItemAdmin)
admin.site.register(RelatedProduct, RelatedProductAdmin)
admin.site.register(Lot, LotAdmin)
admin.site.register(Session, SessionAdmin)
